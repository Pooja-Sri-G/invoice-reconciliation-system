# Privacy-preserving invoice reconciliation

The Streamlit application is the federated client. It reads the three PDFs locally and calls Gemini from that client process. The FastAPI service never receives PDF bytes, filenames, extracted fields, prompts, or reconciliation text.

## Run

From this directory, with the virtual environment active:

```powershell
uvicorn main:app --host 127.0.0.1 --port 8001
streamlit run app.py
```

Set `GEMINI_API_KEY` in the client environment. Set `FEDERATED_CLIENT_ID` to a stable, non-PII identifier for each participating client installation.

## Federated protocol

- `GET /federated/config` returns the current model version and round settings.
- `POST /federated/update` accepts only numeric `weights`, numeric `metrics`, a sample count, and a client identifier.
- `POST /federated/round/close` publishes the weighted FedAvg result and starts the next round after at least two participants have submitted updates.

`federated_learning.py` is shared by the client and coordinator. `build_local_update` converts the local reconciliation result into aggregate signals only; the result text is never included in the request.

## Production hardening

This implementation provides the federated boundary and weighted aggregation, but a production deployment should add authenticated clients, TLS, persistent round storage, replay protection, update clipping, differential privacy noise, and a secure aggregation protocol. The current coordinator stores updates in memory and is intended as a local prototype.
