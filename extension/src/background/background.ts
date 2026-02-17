// Background Service Worker for Veritas AI
console.log('Veritas AI background service worker loaded');

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  if (request.action === 'analyzeArticle') {
    analyzeArticle(request.data)
      .then(result => sendResponse(result))
      .catch(error => {
        console.error('Error analyzing article:', error);
        sendResponse({
          error: 'Failed to analyze article'
        });
      });

    return true; // Keep message channel open for async response
  }
});

async function analyzeArticle(articleData: any) {
  // TODO: Replace with actual API call to backend
  // For now, return mock data

  console.log('Analyzing article:', articleData);

  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // Generate mock analysis based on domain
  const mockData = generateMockAnalysis(articleData.domain, articleData.title);

  return mockData;
}

function generateMockAnalysis(domain: string, title: string) {
  // Generate semi-realistic mock data
  const credibilityScore = Math.floor(Math.random() * 40) + 50; // 50-90

  const biasOptions = ['Left', 'Center-Left', 'Center', 'Center-Right', 'Right'];
  const biasRating = biasOptions[Math.floor(Math.random() * biasOptions.length)];

  // Generate coverage breakdown that adds to 100
  const left = Math.floor(Math.random() * 50) + 10;
  const right = Math.floor(Math.random() * 50) + 10;
  const center = 100 - left - right;

  return {
    credibilityScore,
    biasRating,
    coverage: {
      left,
      center: Math.max(0, center),
      right
    },
    domain,
    title: title.substring(0, 100), // Truncate long titles
    // Additional metadata for future use
    metadata: {
      analyzed: new Date().toISOString(),
      sources: ['Mock Source 1', 'Mock Source 2', 'Mock Source 3']
    }
  };
}

// Extension installation handler
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Veritas AI installed');
  } else if (details.reason === 'update') {
    console.log('Veritas AI updated');
  }
});
