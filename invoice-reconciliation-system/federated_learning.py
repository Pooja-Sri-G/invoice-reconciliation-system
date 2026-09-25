"""Shared client/coordinator protocol for privacy-preserving learning."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Dict, List

from pydantic import BaseModel, Field


MODEL_VERSION = "invoice-reconciliation-1"


class FederatedUpdate(BaseModel):
    """A numeric update; PDFs and extracted fields never enter this model."""

    model_version: str = Field(default=MODEL_VERSION, min_length=1)
    client_id: str = Field(min_length=1, max_length=128)
    sample_count: int = Field(default=1, ge=1, le=1000)
    weights: Dict[str, float] = Field(min_length=1, max_length=32)
    metrics: Dict[str, float] = Field(default_factory=dict, max_length=32)


class AggregatedModel(BaseModel):
    model_version: str
    round_number: int
    weights: Dict[str, float]
    participant_count: int
    sample_count: int
    metrics: Dict[str, float]


def build_local_update(result: str, client_id: str) -> FederatedUpdate:
    """Create a numeric update without sending reconciliation text upstream."""

    normalized = result.upper()
    matched = 1.0 if "STATUS: MATCHED" in normalized else 0.0
    discrepancy_count = float(
        sum(
            1
            for line in result.splitlines()
            if line.strip().startswith("-") and "NONE" not in line.upper()
        )
    )
    return FederatedUpdate(
        client_id=client_id,
        weights={"match_rate": matched, "discrepancy_rate": min(discrepancy_count, 100.0)},
        metrics={"matched_documents": matched, "discrepancy_count": discrepancy_count},
    )


@dataclass
class FederatedCoordinator:
    """In-memory FedAvg coordinator for a single running API instance."""

    model_version: str = MODEL_VERSION
    minimum_participants: int = 2

    def __post_init__(self) -> None:
        self._round_number = 1
        self._updates: List[FederatedUpdate] = []
        self._lock = Lock()

    def add_update(self, update: FederatedUpdate) -> AggregatedModel:
        if update.model_version != self.model_version:
            raise ValueError(
                f"Unsupported model version: {update.model_version}. Expected {self.model_version}."
            )
        with self._lock:
            self._updates.append(update)
            return self._aggregate_locked()

    def current_model(self) -> AggregatedModel:
        with self._lock:
            return self._aggregate_locked()

    def _aggregate_locked(self) -> AggregatedModel:
        if not self._updates:
            return AggregatedModel(
                model_version=self.model_version,
                round_number=self._round_number,
                weights={},
                participant_count=0,
                sample_count=0,
                metrics={},
            )

        total_samples = sum(update.sample_count for update in self._updates)
        weight_totals: Dict[str, float] = {}
        metric_totals: Dict[str, float] = {}
        for update in self._updates:
            for name, value in update.weights.items():
                weight_totals[name] = weight_totals.get(name, 0.0) + value * update.sample_count
            for name, value in update.metrics.items():
                metric_totals[name] = metric_totals.get(name, 0.0) + value * update.sample_count

        return AggregatedModel(
            model_version=self.model_version,
            round_number=self._round_number,
            weights={name: value / total_samples for name, value in weight_totals.items()},
            participant_count=len(self._updates),
            sample_count=total_samples,
            metrics={name: value / total_samples for name, value in metric_totals.items()},
        )

    def close_round(self) -> AggregatedModel:
        with self._lock:
            model = self._aggregate_locked()
            if model.participant_count < self.minimum_participants:
                raise ValueError(
                    f"At least {self.minimum_participants} participants are required before closing a federated round."
                )
            self._updates.clear()
            self._round_number += 1
            return model
