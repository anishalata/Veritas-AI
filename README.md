# Veritas AI

An AI-powered Chrome extension for fake news detection and media bias analysis.

## Project Overview

Veritas AI helps users evaluate the credibility and bias of online news articles in real-time. The extension analyzes articles and provides:

- **Credibility Score** (0-100): Overall trustworthiness assessment
- **Bias Spectrum**: Political leaning classification (Left to Right)
- **Coverage Breakdown**: Distribution of sources across the political spectrum

## Current Status: Phase 0 & 1 ✅

**Completed:**
- ✅ Chrome Extension skeleton (Manifest V3)
- ✅ React + TypeScript popup UI
- ✅ Article extraction with Mozilla Readability
- ✅ Background service worker architecture
- ✅ Mock data pipeline

**Currently Using Mock Data** - Real AI analysis coming in Phase 2-3

## How It Works

### Current Architecture (Phase 1)

```
┌──────────────┐
│   Browser    │
│  (Any Site)  │
└──────┬───────┘
       │
       │ User clicks extension icon
       ▼
┌──────────────────────────────────────┐
│     Veritas AI Extension             │
│  ┌────────────────────────────────┐  │
│  │  Popup UI (React)              │  │
│  │  - Analyze button              │  │
│  │  - Results panels              │  │
│  └───────┬────────────────────────┘  │
│          │                            │
│          │ (1) Request extraction     │
│          ▼                            │
│  ┌────────────────────────────────┐  │
│  │  Content Script                │  │
│  │  - Mozilla Readability         │  │
│  │  - Extracts article content    │  │
│  └───────┬────────────────────────┘  │
│          │                            │
│          │ (2) Send article data      │
│          ▼                            │
│  ┌────────────────────────────────┐  │
│  │  Service Worker                │  │
│  │  - Currently: mock data        │  │
│  │  - Future: API calls           │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

### Future Architecture (Phase 2-3)

```
┌──────────────────────────────────────┐
│     Veritas AI Extension             │
│  (Chrome Browser)                    │
└───────────────┬──────────────────────┘
                │
                │ HTTPS API Request
                ▼
┌──────────────────────────────────────┐
│     Backend API (FastAPI)            │
│  ┌────────────────────────────────┐  │
│  │  Analysis Pipeline             │  │
│  │  1. Source credibility check   │  │
│  │  2. Bias classification        │  │
│  │  3. Cross-reference validation │  │
│  └────────┬───────────────────────┘  │
│           │                           │
│           ▼                           │
│  ┌────────────────────────────────┐  │
│  │  ML Model (LLM)                │  │
│  │  - Credibility scoring         │  │
│  │  - Bias detection              │  │
│  │  - Claim verification          │  │
│  └────────┬───────────────────────┘  │
│           │                           │
│           ▼                           │
│  ┌────────────────────────────────┐  │
│  │  External Data Sources         │  │
│  │  - NewsAPI / GDELT             │  │
│  │  - Fact-check databases        │  │
│  │  - Source reputation DB        │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

### Analysis Flow

1. **User opens article** → Extension icon activates
2. **User clicks "Analyze"** → Content script extracts article using Readability
3. **Article sent to service worker** → Forwards to backend API
4. **Backend analyzes**:
   - Checks source credibility against database
   - ML model scores article content
   - Cross-references claims with fact-check databases
   - Analyzes political bias indicators
5. **Results returned** → Displayed in three panels (Credibility, Bias, Coverage)

## Project Structure

```
veritas-ai/
├── extension/      # Chrome extension (React + TypeScript)
├── api/           # Backend API (TODO: FastAPI)
├── model/         # ML models (TODO: Fine-tuned LLM)
├── docs/          # Documentation
└── README.md
```

## Quick Start

See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions.

**TL;DR:**
```bash
cd extension
npm install
npm run build
# Load extension/dist/ in Chrome
```

## Roadmap

- [x] **Phase 0:** Project setup and planning
- [x] **Phase 1:** Chrome extension skeleton with mock data
- [ ] **Phase 2:** Backend API (FastAPI + PostgreSQL)
- [ ] **Phase 3:** ML model integration (LLM fine-tuning)
- [ ] **Phase 4:** Real-time fact checking
- [ ] **Phase 5:** Cross-reference validation
- [ ] **Phase 6:** User feedback and iteration

## Tech Stack

### Extension (Current)
- React + TypeScript
- Vite (bundler)
- Chrome Manifest V3
- Mozilla Readability

### Backend (Planned)
- FastAPI
- PostgreSQL
- Redis (caching)
- NewsAPI / GDELT

### ML (Planned)
- Fine-tuned LLM (GPT-4 or open-source alternative)
- Vector embeddings for semantic search
- Bias detection model

## Contributing

This is currently a solo project in active development. Stay tuned for contribution guidelines!

## License

TBD
