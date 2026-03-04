# LangChain Agent API

One endpoint: **POST /api/chat** — send `{ "message": "your text" }`, get `{ "reply": "..." }`.

**Run** (from project root):  
`uvicorn src.api.app:app --reload --port 8000`  
Docs: http://localhost:8000/docs

---

## What each file does

**app.py**  
- Adds project root and `src` to `sys.path` so imports like `agents.agent` and `rag.rag_wrapper` work when you run from the repo root.  
- **lifespan**: When the server starts, it builds the agent once and stores it in `app.state.agent`. When the server stops, it closes the SQLite DB used for conversation memory.  
- **CORS**: Allows the Angular app on `http://localhost:4200` to call this API from the browser.  
- Mounts the chat router under `/api`, so the only route is `POST /api/chat`.

**schemas.py**  
- **ChatRequest**: Expects a JSON body with `message` (required) and optional `thread_id`. Same `thread_id` = same conversation (memory).  
- **ChatResponse**: JSON with one field, `reply` (the agent’s answer).  
FastAPI uses these to check incoming JSON and to document the API.

**routes/chat.py**  
- **POST /chat**: Reads `message` and optional `thread_id` from the body.  
- Gets the shared agent from `request.app.state.agent`.  
- Calls your existing `rag_enhanced_agent_invoke(agent, inputs, config)` — same as the CLI.  
- Takes the last message from the response and returns its text as `reply`.
