import { Readability } from '@mozilla/readability';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  if (request.action === 'extractArticle') {
    try {
      const articleData = extractArticle();

      if (articleData) {
        sendResponse({
          success: true,
          data: articleData
        });
      } else {
        sendResponse({
          success: false,
          error: 'Could not extract article content'
        });
      }
    } catch (error) {
      console.error('Error extracting article:', error);
      sendResponse({
        success: false,
        error: 'Error extracting article content'
      });
    }
  }

  return true; // Keep message channel open for async response
});

function extractArticle() {
  try {
    // Get the domain
    const domain = window.location.hostname;

    // Clone the document for Readability
    const documentClone = document.cloneNode(true) as Document;

    // Use Readability to extract article content
    const reader = new Readability(documentClone);
    const article = reader.parse();

    if (!article) {
      // Fallback: try to extract basic content
      return {
        domain: domain,
        title: document.title || 'Unknown Title',
        textContent: document.body.innerText.substring(0, 5000), // First 5000 chars
        excerpt: document.querySelector('meta[name="description"]')?.getAttribute('content') || '',
        url: window.location.href
      };
    }

    return {
      domain: domain,
      title: article.title,
      textContent: article.textContent,
      excerpt: article.excerpt,
      url: window.location.href,
      byline: article.byline,
      siteName: article.siteName
    };
  } catch (error) {
    console.error('Error in extractArticle:', error);
    return null;
  }
}

// Log that content script is loaded
console.log('Veritas AI content script loaded');
