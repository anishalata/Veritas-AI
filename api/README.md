# Veritas AI - Backend API

FastAPI backend for article credibility analysis.

## Setup

1. **Create virtual environment:**
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your NewsAPI key (optional for Phase 2)
   ```

4. **Run the server:**
   ```bash
   python main.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### `POST /analyze`

Analyze an article for credibility and bias.

**Request:**
```json
{
  "domain": "cnn.com",
  "title": "Article title",
  "textContent": "Full article text...",
  "excerpt": "Summary",
  "url": "https://example.com/article",
  "byline": "Author name",
  "siteName": "CNN"
}
```

**Response:**
```json
{
  "credibilityScore": 78,
  "biasRating": "Center-Left",
  "coverage": {
    "left": 45,
    "center": 30,
    "right": 25
  },
  "domain": "cnn.com",
  "title": "Article title",
  "metadata": {
    "sourceCredibility": 78,
    "contentScore": 75,
    "analyzed": "server"
  }
}
```

## Phase 2 Features

- ✅ Source credibility database (40+ news sources)
- ✅ Bias classification
- ✅ Basic content analysis (clickbait detection)
- ✅ Coverage breakdown (simulated)
- ⏳ NewsAPI integration (Phase 2.5)

## Phase 3 (Planned)

- ML model for credibility scoring
- Fine-tuned LLM for bias detection
- Claim verification
- Semantic similarity search

## Testing

```bash
# Test the API
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "cnn.com",
    "title": "Test Article",
    "textContent": "Article content here",
    "url": "https://example.com"
  }'
```

## Development

Server runs on `http://localhost:8000` by default.

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
