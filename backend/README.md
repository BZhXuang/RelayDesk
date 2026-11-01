# RelayDesk API (Python)

FastAPI service for RelayDesk. See the root [README](../README.md) for product behavior, architecture, setup, evaluation scope, and security notes.

From this directory, install `requirements-dev.txt`, configure a local `.env`, and start Redis and ChromaDB. Then run:

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Interactive API documentation is available at `/docs`. Key routes include:

- `GET /health` — readiness.
- `POST /chat` — multi-turn support request.
- `POST /search`, `/knowledge/add`, `/knowledge/upload` — knowledge retrieval and ingestion.
- `GET /trace/tool/{request_id}` — request tool trace.
- `POST /eval/run`, `GET /eval/jobs/{job_id}` — evaluation jobs.
- `GET /monitor`, `GET /metrics` — runtime monitoring.
- `/mcp/` — standard MCP endpoint for local knowledge tools.

Run backend tests with `python -m pytest tests -q`. Most automated checks use mocks or in-memory fakes; they do not measure provider quality or production capacity.
