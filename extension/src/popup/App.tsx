import { useState } from 'react';

interface AnalysisResult {
  credibilityScore: number;
  biasRating: string;
  coverage: {
    left: number;
    center: number;
    right: number;
  };
  domain: string;
  title: string;
  reasons: string[];
  isNewsArticle: boolean;
  detectionMessage: string;
}

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [extractError, setExtractError] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);
    setExpanded(null);
    setExtractError(false);

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab.id) {
      setLoading(false);
      return;
    }

    chrome.tabs.sendMessage(
      tab.id,
      { action: 'extractArticle' },
      (response) => {
        if (response && response.success) {
          chrome.runtime.sendMessage(
            { action: 'analyzeArticle', data: response.data },
            (analysisResult) => {
              setResult(analysisResult);
              setLoading(false);
            }
          );
        } else {
          setExtractError(true);
          setLoading(false);
        }
      }
    );
  };

  const toggle = (panel: string) => {
    setExpanded(expanded === panel ? null : panel);
  };

  const scoreColor = (score: number) =>
    score >= 70 ? '#22c55e' : score >= 40 ? '#f59e0b' : '#ef4444';

  const scoreLabel = (score: number) =>
    score >= 70 ? 'High Credibility' : score >= 40 ? 'Moderate Credibility' : 'Low Credibility';

  const reasonsSentence = (reasons: string[]) =>
    reasons.length > 0 ? reasons.join('. ') + '.' : '';

  return (
    <div className="popup-container">
      <header className="header">
        <h1>Veritas AI</h1>
        <p className="tagline">AI-Powered Fact Checking</p>
      </header>

      <button
        className="analyze-btn"
        onClick={handleAnalyze}
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Analyze Article'}
      </button>

      {extractError && (
        <div className="not-news-banner">
          <span className="not-news-icon">⚠️</span>
          <p>Could not extract article content from this page.</p>
        </div>
      )}

      {result && !result.isNewsArticle && (
        <div className="not-news-banner">
          <span className="not-news-icon">⚠️</span>
          <p>This isn't a news article, so we can't analyze it.</p>
        </div>
      )}

      {result && result.isNewsArticle && (
        <div className="results">
          <p className="article-domain">Source: {result.domain.replace('www.', '').split('.')[0].toUpperCase()}</p>

          {/* Credibility Score — always visible */}
          <div className="score-row">
            <span className="score-big" style={{ color: scoreColor(result.credibilityScore) }}>
              {result.credibilityScore}
            </span>
            <div className="score-meta">
              <span className="score-label-text" style={{ color: scoreColor(result.credibilityScore) }}>
                {scoreLabel(result.credibilityScore)}
              </span>
              <div className="score-sub">out of 100</div>
            </div>
          </div>

          {/* Reasons — sentence form */}
          {result.reasons && result.reasons.length > 0 && (
            <p className="reasons-text">{reasonsSentence(result.reasons)}</p>
          )}

          {/* Expandable: Bias */}
          <div className="accordion">
            <button className="accordion-header" onClick={() => toggle('bias')}>
              <span>Bias Spectrum</span>
              <span className="accordion-value">{result.biasRating}</span>
              <span className="chevron">{expanded === 'bias' ? '▲' : '▼'}</span>
            </button>
            {expanded === 'bias' && (
              <div className="accordion-body">
                <div className="bias-bar">
                  <div className="bias-indicator" style={{
                    left: result.biasRating === 'Left' ? '10%' :
                          result.biasRating === 'Center-Left' ? '30%' :
                          result.biasRating === 'Center' ? '50%' :
                          result.biasRating === 'Center-Right' ? '70%' : '90%'
                  }}></div>
                </div>
                <div className="bias-labels">
                  <span>Left</span>
                  <span>Center</span>
                  <span>Right</span>
                </div>
                <p className="bias-note">This outlet is typically rated <strong>{result.biasRating}</strong> by Media Bias/Fact Check. This reflects the source's overall political lean, not the specific article.</p>
              </div>
            )}
          </div>

          {/* Expandable: Coverage */}
          <div className="accordion">
            <button className="accordion-header" onClick={() => toggle('coverage')}>
              <span>Coverage Breakdown</span>
              <span className="accordion-value">{result.coverage.left}L / {result.coverage.center}C / {result.coverage.right}R</span>
              <span className="chevron">{expanded === 'coverage' ? '▲' : '▼'}</span>
            </button>
            {expanded === 'coverage' && (
              <div className="accordion-body">
                <p className="coverage-note">
                  Of the outlets covering this story, {result.coverage.left}% lean left, {result.coverage.center}% are center, and {result.coverage.right}% lean right.
                </p>
                <div className="coverage-bubbles">
                  <div className="coverage-bubble left">
                    <span className="bubble-percent">{result.coverage.left}%</span>
                    <span className="bubble-label">Left</span>
                  </div>
                  <div className="coverage-bubble center">
                    <span className="bubble-percent">{result.coverage.center}%</span>
                    <span className="bubble-label">Center</span>
                  </div>
                  <div className="coverage-bubble right">
                    <span className="bubble-percent">{result.coverage.right}%</span>
                    <span className="bubble-label">Right</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
