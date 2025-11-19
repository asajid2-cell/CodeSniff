# CodeSniff

Semantic code search engine with natural language queries, file upload indexing, and conversational code assistance.

## Features

**Semantic Search** - Find code using plain English instead of exact keywords
**Hybrid Search** - Combines BM25 text matching with CodeBERT embeddings for accurate results
**Upload & Index** - Drag-and-drop folders, ZIP files, or clone GitHub repositories
**Code Chat** - Groq-powered chatbot answers questions about your codebase with RAG
**Real-time Search** - Debounced queries with 40% minimum similarity threshold
**Modern UI** - Clean GitHub/Linear-style interface with dark mode

## Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- 4GB RAM minimum

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

python -m app.main
```

Server runs on http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

App runs on http://localhost:5173

## Configuration

Edit `backend/.env` with your credentials:

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Required for chatbot feature (get from console.groq.com) |

## Usage

### Indexing Code

**Upload via UI:**
1. Click upload button in header
2. Select folder, ZIP file, or enter GitHub URL
3. Wait for automatic indexing

**Via API:**
```bash
# Index local directory
curl -X POST http://localhost:8000/api/index \
  -H "Content-Type: application/json" \
  -d '{"directory_path": "/path/to/project"}'

# Clone and index GitHub repo
curl -X POST http://localhost:8000/api/index/github \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo"}'
```

### Searching

**Example queries:**
- "functions that validate email addresses"
- "code that connects to postgres"
- "error handling for API requests"
- "authentication middleware"

**Via UI:**
Type query in search bar, press Enter

**Via API:**
```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "email validation", "limit": 20, "min_similarity": 0.4}'
```

### Code Chat

**Via UI:**
Click chat icon, toggle "Search codebase for context" for RAG

**Via API:**
```bash
curl -X POST "http://localhost:8000/api/chat?message=How does the search engine work?&use_rag=true" \
  -H "Content-Type: application/json" \
  -d '[]'
```

## API Endpoints

### Indexing
- `POST /api/index` - Index local directory
- `POST /api/index/github` - Clone and index GitHub repo
- `POST /api/index/upload` - Upload and index files
- `POST /api/index/clear` - Clear all indexed data
- `GET /api/files` - List indexed files

### Search
- `POST /api/search` - Semantic search
- `POST /api/search/name` - Search by symbol name
- `POST /api/search/similar` - Find similar code
- `GET /api/symbol/<name>` - Get specific symbol

### Chat
- `POST /api/chat` - Chat with codebase assistant

### System
- `GET /api/stats` - Index statistics
- `GET /api/health` - Health check

Full API docs: http://localhost:8000/docs

## Project Structure

```
backend/
  app/
    main.py              # FastAPI application
    api/routes.py        # API endpoints
    core/
      parser.py          # Tree-sitter code parsing
      embedder.py        # CodeBERT embeddings
      indexer.py         # Indexing pipeline
      search.py          # Semantic search
      text_search.py     # BM25 text search
    chatbot/
      groq_chat.py       # Groq chatbot with RAG
    storage/
      vector_store.py    # FAISS vector index
      metadata_store.py  # SQLite metadata
    utils/
      github_clone.py    # GitHub cloning utilities

frontend/
  src/
    components/
      SearchBar.tsx      # Search interface
      ResultCard.tsx     # Result display
      ChatPanel.tsx      # Chat interface
      UploadModal.tsx    # File upload UI
    hooks/
      useSearch.ts       # Search logic
      useStats.ts        # Stats fetching
    api/client.ts        # API client
```

## Tech Stack

**Backend:**
- FastAPI - Web framework
- CodeBERT - Microsoft's code embeddings model
- FAISS - Facebook's vector similarity search
- Tree-sitter - Fast code parsing
- BM25 - Text search algorithm
- Groq - LLM inference (llama-3.3-70b-versatile)
- SQLite - Metadata storage

**Frontend:**
- React 18 + TypeScript
- Tailwind CSS - Styling
- Framer Motion - Animations
- Lucide Icons - Icon library
- Axios - HTTP client

## Performance

- **Indexing**: ~1000 LOC/second
- **Search**: <100ms for 10,000+ symbols
- **Memory**: ~1MB per 1000 symbols
- **Similarity Threshold**: 40% minimum to filter noise

## File Cleaning

Automatic cleanup during GitHub/upload indexing removes:
- Media files (images, audio, video)
- Archives (zip, tar, etc.)
- Binaries and executables
- node_modules, __pycache__, .git
- Large data files (>1MB JSON/CSV)
- Fonts, PDFs, Office documents

Only Python and JavaScript/TypeScript files are indexed.

## License

MIT
