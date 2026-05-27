# CLAUDE.md - AI Semiconductor Export Regulation Risk Analysis Agent

## Project Overview
A RAG-based system that receives user questions about semiconductor export,
retrieves relevant regulation clauses via vector search, and streams LLM risk analysis in real-time.

---

## Tech Stack
| Category | Technology |
|----------|------------|
| Language | Python 3.10 |
| Backend | FastAPI, Uvicorn |
| Vector DB | Qdrant (local file mode) |
| Embedding | SentenceBERT (`jhgan/ko-sroberta-multitask`, 768-dim) |
| LLM | OpenAI API (gpt-4o-mini) |
| Streaming | SSE (Server-Sent Events) |
| Frontend | Single HTML + JavaScript file |

---

## Directory Structure
```
mini/
├── data/
│   └── regulations.csv      # Raw regulation data (Korean)
├── docs/
│   ├── plan.md              # Project plan & role assignments
│   ├── ARCHITECTURE.md      # System architecture & flowcharts
│   ├── DATA_SCHEMA.md       # Data structure definitions
│   ├── API_SPEC.md          # API endpoint specifications
│   └── CODE_FLOW.md         # Code execution flow explanation
├── templates/
│   └── index.html           # Frontend UI (TODO)
├── qdrant_db/               # Qdrant local storage (auto-generated, gitignored)
├── ingest.py                # Embed CSV data → store in Qdrant (run once)
├── inspect_db.py            # CLI tool to inspect Qdrant DB contents
├── search.py                # CLI tool to test vector search
├── api.py                   # FastAPI server - main backend (WIP)
├── CLAUDE.md                # This file
└── requirements.txt         # Python dependencies
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set environment variables
Create `.env` in root:
```
OPENAI_API_KEY=sk-...
```

### 3. Load data (run once)
```bash
python ingest.py
```

---

## Commands
```bash
# Load data into Qdrant (once only)
python ingest.py

# Test vector search via CLI
python search.py

# Run API server
uvicorn api:app --reload

# Access server
http://localhost:8000
```

---

## Architecture Flow
```
User question
    → POST /query (FastAPI)
    → SentenceBERT → 768-dim vector
    → Qdrant cosine similarity search → Top 3 regulation clauses
    → Inject clauses into prompt (RAG)
    → OpenAI API call (stream=True)
    → SSE stream to frontend
```

---

## Important Notes
- `ingest.py`, `search.py`, `api.py` must all use the **same embedding model**
- Qdrant vector size (`size=768`) must match model output dimension
- `qdrant_db/` is gitignored (large binary files)
- Data and responses are in **Korean** — embedding model supports Korean
