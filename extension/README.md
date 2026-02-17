# Veritas AI - Chrome Extension

AI-powered fake news detection and media bias analysis Chrome extension.

## Phase 0 & 1 - Current Status

This is the initial skeleton implementation with:
- ✅ Manifest V3 configuration
- ✅ React + TypeScript popup UI
- ✅ Content script with Mozilla Readability for article extraction
- ✅ Background service worker (currently returns mock data)
- ✅ Three analysis panels: Credibility Score, Bias Spectrum, Coverage Breakdown

## Architecture & Message Flow

### Components

| Component | File | Runs Where | Purpose |
|-----------|------|------------|---------|
| **Popup UI** | `src/popup/App.tsx` | Extension popup window | User interface with Analyze button and results panels |
| **Content Script** | `src/content/content.ts` | Inside web pages | Extracts article content using Mozilla Readability |
| **Service Worker** | `src/background/background.ts` | Background process | Handles API calls and data processing |

### How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. User clicks "Analyze Article" button in popup               │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Popup sends message to Content Script:                      │
│    { action: 'extractArticle' }                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Content Script uses Mozilla Readability to extract:         │
│    - Domain (e.g., "cnn.com")                                   │
│    - Title                                                      │
│    - Body text (cleaned of ads, navigation, etc.)               │
│    - Excerpt/summary                                            │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Content Script sends extracted data back to Popup           │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. Popup sends article data to Service Worker:                 │
│    { action: 'analyzeArticle', data: {...} }                    │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Service Worker processes the request:                       │
│    - Currently: generates mock data                             │
│    - Future (Phase 2): calls backend API                        │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. Service Worker returns analysis results:                    │
│    {                                                            │
│      credibilityScore: 75,                                      │
│      biasRating: "Center-Left",                                 │
│      coverage: { left: 35, center: 40, right: 25 }              │
│    }                                                            │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. Popup displays results in three panels:                     │
│    - Credibility Score (0-100 circular meter)                   │
│    - Bias Spectrum (Left ← → Right slider)                      │
│    - Coverage Breakdown (3 bar charts)                          │
└─────────────────────────────────────────────────────────────────┘
```

### Why This Architecture?

- **Content Script** runs in the context of web pages, so it can access and extract article DOM
- **Service Worker** handles background processing and API calls without blocking UI
- **Popup** provides a clean separation of UI logic from data extraction/processing
- **Message passing** keeps components decoupled and maintains security boundaries

## Setup Instructions

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Build the extension:**
   ```bash
   npm run build
   ```

3. **Load in Chrome:**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right)
   - Click "Load unpacked"
   - Select the `dist` folder from this directory

4. **Test the extension:**
   - Navigate to any news article
   - Click the Veritas AI extension icon
   - Click "Analyze Article" button
   - You should see mock analysis results

## Development

- `npm run dev` - Start development mode with hot reload
- `npm run build` - Build for production

## Project Structure

```
extension/
├── src/
│   ├── popup/          # React popup UI
│   │   ├── App.tsx     # Main popup component
│   │   ├── popup.tsx   # Popup entry point
│   │   └── popup.css   # Popup styles
│   ├── content/        # Content scripts
│   │   └── content.ts  # Article extraction with Readability
│   └── background/     # Background service worker
│       └── background.ts  # API communication (mock data)
├── public/
│   ├── manifest.json   # Chrome extension manifest
│   └── icons/          # Extension icons (TODO: add actual icons)
└── dist/              # Built extension (generated)
```

## Next Steps

- [ ] Add actual extension icons (16x16, 48x48, 128x128)
- [ ] Implement backend API
- [ ] Replace mock data with real analysis
- [ ] Add error handling and loading states
- [ ] Implement caching
- [ ] Add settings page

## Notes

- Currently uses **mock data** for all analysis
- Readability extraction works on most article pages
- Background service worker is ready to connect to backend API
