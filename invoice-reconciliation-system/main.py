from fastapi import FastAPI, HTTPException

from federated_learning import (
    AggregatedModel,
    FederatedCoordinator,
    FederatedUpdate,
    MODEL_VERSION,
)

app = FastAPI(title="Invoice Reconciliation API")
coordinator = FederatedCoordinator()


@app.get("/")
def home():
    return {"status": "FastAPI is running!"}


@app.get("/federated/config")
def federated_config():
    return {
        "model_version": MODEL_VERSION,
        "round_number": coordinator.current_model().round_number,
        "minimum_participants": coordinator.minimum_participants,
        "privacy": "PDFs and extracted document fields are processed client-side.",
    }


@app.post("/federated/update", response_model=AggregatedModel)
def submit_federated_update(update: FederatedUpdate):
    try:
        return coordinator.add_update(update)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/federated/round/close", response_model=AggregatedModel)
def close_federated_round():
    try:
        return coordinator.close_round()
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error