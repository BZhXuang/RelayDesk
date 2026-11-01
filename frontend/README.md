# RelayDesk Web Console

Vue 3 interface for the Python service. See the [main README](../README.md) for architecture, setup, and configuration.

```bash
npm ci
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api/python/*` to `http://localhost:8000`; `VITE_PYTHON_API_URL` overrides the target. The production container proxies the same path to `relaydesk-api`.

The console supports multi-turn chat, knowledge import/search, evaluation jobs, health and monitoring views, and tool-trace inspection. The model API key belongs only in the backend environment and is not sent to the browser.

```bash
npm test
npm run build
```
