# Veritas AI - Quick Start Guide

Everything you need to run Veritas AI locally from scratch.

---

## Prerequisites

Make sure you have these installed:
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://www.python.org/) (v3.9 or higher)
- Google Chrome

---

## Step 1: Get a NewsAPI Key

Veritas AI uses NewsAPI to show real coverage data across left/center/right outlets.

1. Go to [https://newsapi.org](https://newsapi.org) and click **Get API Key**
2. Sign up for a free account
3. Copy your API key — you'll need it in Step 3

Free tier gives you 100 requests/day which is enough for development and demos.

---

## Step 2: Train the ML Model

The credibility scoring uses a machine learning model trained on the LIAR dataset. You need to train it once before running the API.

```bash
cd model

# Install model dependencies
pip install -r requirements.txt

# Train the model (takes 1-2 minutes)
python train.py
```

This saves the trained model to `model/models/credibility_model.pkl`. You only need to do this once.

---

## Step 3: Set Up the Backend API

```bash
cd api

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Create your .env file
cp .env.example .env
```

Now open `api/.env` and add your NewsAPI key:

```
NEWSAPI_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
```

Then start the server:

```bash
python main.py
```

Server runs at **http://localhost:8000** — keep this terminal open.

---

## Step 4: Build the Chrome Extension

Open a new terminal:

```bash
cd extension

# Install dependencies
npm install

# Build the extension
npm run build
```

This creates a `dist/` folder with the compiled extension.

---

## Step 5: Load the Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in the top right)
3. Click **Load unpacked**
4. Select the `extension/dist/` folder
5. Veritas AI should now appear in your extensions list

---

## Step 6: Use It

1. Navigate to any news article (CNN, BBC, Fox News, Reuters, etc.)
2. Click the **Veritas AI** icon in your Chrome toolbar
3. Click **Analyze Article**
4. You'll see:
   - **Credibility Score** — 0 to 100 with plain-English reasons
   - **Bias Spectrum** — where this outlet sits politically
   - **Coverage Breakdown** — how left/center/right outlets are covering this story

---

## How It Works

```
[Chrome Extension]
       |
       | 1. Extracts article text using Mozilla Readability
       |
       ▼
[FastAPI Backend at localhost:8000]
       |
       | 2. Looks up source credibility (40+ news sources)
       | 3. Runs ML model on article text (TF-IDF + Logistic Regression)
       | 4. Runs heuristic checks (sensational language, source attribution, etc.)
       | 5. Calls NewsAPI to find real coverage across outlets
       |
       ▼
[Score returned to extension]
   Final Score = (Source Credibility × 60%) + (ML + Heuristics × 40%)
```

---

## Testing the API Directly

You can test the backend without the extension:

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

Or visit **http://localhost:8000/docs** for the interactive API docs.

---

## Troubleshooting

**"Could not extract article content"**
- Make sure you're on an actual article page, not a homepage
- Try a mainstream news site like CNN or BBC first
- Some paywalled sites may block extraction

**API not responding**
- Make sure `python main.py` is still running in your terminal
- Check that your virtual environment is activated
- Try visiting http://localhost:8000/health — it should return `{"status": "healthy"}`

**Coverage always showing 33/33/33**
- Your NewsAPI key may be missing or invalid — check `api/.env`
- You may have hit the 100 requests/day free tier limit

**Extension not updating after code changes**
- Run `npm run build` in the `extension/` folder
- Go to `chrome://extensions/` and click the reload icon on Veritas AI
