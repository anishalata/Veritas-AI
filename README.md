# Veritas AI

An AI-powered Chrome extension that analyzes news articles for credibility, political bias, and media coverage in real time.

## What It Does

- **Credibility Score** (0–100): Combines source reputation, ML model, and heuristic signals
- **Bias Spectrum**: Political leaning classification (Left to Right)
- **Coverage Breakdown**: How many left/center/right outlets are covering the same story
- **Non-Article Detection**: Automatically detects if the page is not a news article and tells you why

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/anishalata/Veritas-AI
cd veritas-ai
```

### 2. Set up the API

```bash
cd api
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

You'll need to run `source venv/bin/activate` each time you open a new terminal before starting the API.

Then install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `api/` folder:

```
NEWSAPI_KEY=your_newsapi_key_here
OPENAI_API_KEY=your_openai_api_key_here

HOST=0.0.0.0
PORT=8000
```

- Get a NewsAPI key at [newsapi.org](https://newsapi.org)
- Get an OpenAI key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 3. Run the API

```bash
cd api
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Keep this terminal open.

### 4. Build the extension

Open a new terminal:

```bash
cd extension
npm install
npm run build
```

### 5. Load in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top-right corner)
3. Click **Load unpacked**
4. Select the `extension/dist/` folder
5. Veritas AI will appear in your extensions list

### 6. Use it

1. Navigate to any news article (CNN, BBC, AP News, etc.)
2. Click the Veritas AI extension icon in your Chrome toolbar
3. Click **Analyze Article**

## After Making Code Changes

Any time you edit the extension code, rebuild and reload:

```bash
cd extension
npm run build
```

Then go to `chrome://extensions/` and click the reload icon on the Veritas AI card.

If you edit the API code, `uvicorn --reload` picks up changes automatically.

## How It Works

```
Browser Tab
    │
    │ User clicks Analyze
    ▼
Content Script (Mozilla Readability)
    │ Extracts title, text, domain
    │ Falls back to tab title if extraction fails
    ▼
Background Service Worker
    │ Sends article data to API
    ▼
FastAPI Backend (localhost:8000)
    │
    ├── OpenAI (gpt-4o-mini) → Is this a news article?
    │       If NO → return content type label (SOCIAL_MEDIA, PRODUCT, VIDEO, etc.)
    │
    ├── Source Credibility DB → score based on domain
    ├── ML Model → fake/real prediction
    ├── Heuristics → sensational language, attribution, length
    └── NewsAPI → coverage across left/center/right outlets
    │
    ▼
Extension Popup
    Displays score, bias, coverage — or explains why it can't analyze the page
```

## Project Structure

```
veritas-ai/
├── api/
│   ├── main.py                      # FastAPI app, /analyze endpoint
│   ├── requirements.txt
│   ├── .env                         # Your API keys (never commit this)
│   └── services/
│       ├── analyzer.py              # Orchestrates all analysis steps
│       ├── article_detector.py      # OpenAI-based news article classifier
│       ├── source_credibility.py    # Source credibility + bias database
│       ├── heuristics.py            # Rule-based credibility signals
│       ├── ml_model.py              # ML model prediction
│       └── coverage.py              # NewsAPI political coverage breakdown
└── extension/
    ├── src/
    │   ├── popup/
    │   │   ├── App.tsx              # Main popup UI
    │   │   └── popup.css
    │   ├── content/
    │   │   └── content.ts           # Article extraction (Readability)
    │   └── background/
    │       └── background.ts        # Service worker, API calls
    └── public/
        └── manifest.json

```

## Tech Stack

- **Extension**: React, TypeScript, Vite, Chrome Manifest V3, Mozilla Readability
- **Backend**: FastAPI, Python, httpx
- **APIs**: OpenAI (gpt-4o-mini), NewsAPI
