# Veritas AI - Setup Guide

## Quick Start

### 1. Install Extension Dependencies

```bash
cd extension
npm install
```

### 2. Build the Extension

```bash
npm run build
```

This will create a `dist/` folder with the compiled extension.

### 3. Load in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top-right corner)
3. Click **"Load unpacked"**
4. Navigate to and select the `extension/dist/` folder
5. The Veritas AI extension should now appear in your extensions list

### 4. Test It Out

1. Navigate to any news article (try CNN, BBC, NYTimes, etc.)
2. Click the Veritas AI extension icon in your Chrome toolbar
3. Click the **"Analyze Article"** button
4. You should see mock analysis results with:
   - Credibility Score
   - Bias Spectrum
   - Coverage Breakdown

## Development Mode

For active development with auto-rebuild:

```bash
cd extension
npm run dev
```

Then reload the extension in Chrome after changes:
1. Go to `chrome://extensions/`
2. Click the reload icon on the Veritas AI extension

## Known Issues (Phase 0/1)

- **Icons:** Placeholder icons needed (extension will work but show default icon)
- **Mock Data:** All analysis results are currently randomized mock data
- **Some sites:** Content extraction may fail on sites with unusual layouts or heavy JavaScript

## Troubleshooting

### Extension won't load
- Make sure you've run `npm install` and `npm run build`
- Check that you're loading the `dist/` folder, not the `src/` folder
- Look for errors in Chrome's extension page

### "Analyze" button doesn't work
- Open Chrome DevTools (F12) and check the Console for errors
- Make sure you're on an actual article page (not Google, homepage, etc.)
- Some sites may block content extraction

### Content script errors
- Check the page's Console for errors
- The Readability library works best on standard article formats
- Try a mainstream news site first (CNN, BBC, etc.)

## Next Development Phases

- **Phase 2:** Backend API with FastAPI
- **Phase 3:** ML Model Integration
- **Phase 4:** Real-time fact checking
- **Phase 5:** Cross-referencing and source validation
