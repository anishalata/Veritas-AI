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
}

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);

    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab.id) {
      setLoading(false);
      return;
    }

    // Send message to content script to extract article
    chrome.tabs.sendMessage(
      tab.id,
      { action: 'extractArticle' },
      (response) => {
        if (response && response.success) {
          // Send to background for analysis (currently returns mock data)
          chrome.runtime.sendMessage(
            { action: 'analyzeArticle', data: response.data },
            (analysisResult) => {
              setResult(analysisResult);
              setLoading(false);
            }
          );
        } else {
          setLoading(false);
          alert('Could not extract article content from this page.');
        }
      }
    );
  };

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

      {result && (
        <div className="results">
          <div className="article-info">
            <h3>{result.title}</h3>
            <p className="domain">{result.domain}</p>
          </div>

          {/* Credibility Score Panel */}
          <div className="panel credibility-panel">
            <h2>Credibility Score</h2>
            <div className="score-circle">
              <span className="score-value">{result.credibilityScore}</span>
              <span className="score-label">/100</span>
            </div>
            <p className="score-description">
              {result.credibilityScore >= 70 ? 'High credibility' :
               result.credibilityScore >= 40 ? 'Moderate credibility' :
               'Low credibility'}
            </p>
          </div>

          {/* Bias Spectrum Panel */}
          <div className="panel bias-panel">
            <h2>Bias Spectrum</h2>
            <div className="bias-meter">
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
            </div>
            <p className="bias-rating">{result.biasRating}</p>
          </div>

          {/* Coverage Breakdown Panel */}
          <div className="panel coverage-panel">
            <h2>Coverage Breakdown</h2>
            <div className="coverage-bars">
              <div className="coverage-item">
                <span className="coverage-label">Left-leaning sources</span>
                <div className="coverage-bar-container">
                  <div
                    className="coverage-bar left"
                    style={{ width: `${result.coverage.left}%` }}
                  ></div>
                </div>
                <span className="coverage-percent">{result.coverage.left}%</span>
              </div>
              <div className="coverage-item">
                <span className="coverage-label">Center sources</span>
                <div className="coverage-bar-container">
                  <div
                    className="coverage-bar center"
                    style={{ width: `${result.coverage.center}%` }}
                  ></div>
                </div>
                <span className="coverage-percent">{result.coverage.center}%</span>
              </div>
              <div className="coverage-item">
                <span className="coverage-label">Right-leaning sources</span>
                <div className="coverage-bar-container">
                  <div
                    className="coverage-bar right"
                    style={{ width: `${result.coverage.right}%` }}
                  ></div>
                </div>
                <span className="coverage-percent">{result.coverage.right}%</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
