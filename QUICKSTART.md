# Veritas AI - Quick Start Guide

## Phase 2 Setup: Run the Full Stack

### 1. Start the Backend API

```bash
cd api

# Create virtual environment (first time only)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the server
python main.py
```

Server will run on: **http://localhost:8000**

### 2. Rebuild the Extension

```bash
cd extension
npm run build
```

### 3. Reload Extension in Chrome

1. Go to `chrome://extensions/`
2. Click the **reload icon** on Veritas AI
3. Navigate to a news article
4. Click the extension icon
5. Click **"Analyze Article"**

---

## How It Works Now

**Phase 2 Flow:**
1. Extension extracts article using Mozilla Readability
2. **Service worker calls real backend API** at `localhost:8000`
3. Backend analyzes article using:
   - **Source credibility database** (40+ news sources)
   - **Bias classification**
   - **Content analysis** (clickbait detection)
4. Real analysis returned to extension
5. Results displayed in UI

**Fallback:** If API is not running, mock data is still used

---

## Testing

### Test the API directly:

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "cnn.com",
    "title": "Breaking News: Major Event Happening",
    "textContent": "Full article text here...",
    "url": "https://cnn.com/article"
  }'
```

### View API docs:

http://localhost:8000/docs

---

## What's Different from Phase 1?

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| Credibility Score | Random (50-90) | **Real source credibility + content analysis** |
| Bias Rating | Random | **From source database (40+ sources)** |
| Coverage | Random distribution | **Semi-intelligent distribution based on bias** |
| Backend | Mock data in extension | **Real FastAPI server** |

---

## Next Steps (Phase 3)

- Add ML model for content credibility
- Integrate NewsAPI for real coverage data
- Fine-tune LLM for bias detection
- Add claim verification
