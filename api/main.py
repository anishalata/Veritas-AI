from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Veritas AI API",
    description="Backend API for fake news detection and media bias analysis",
    version="0.1.0"
)

# Enable CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ArticleRequest(BaseModel):
    domain: str
    title: str
    textContent: str
    excerpt: Optional[str] = None
    url: str
    byline: Optional[str] = None
    siteName: Optional[str] = None

class AnalysisResponse(BaseModel):
    credibilityScore: int
    biasRating: str
    coverage: dict
    domain: str
    title: str
    metadata: dict

@app.get("/")
async def root():
    return {
        "message": "Veritas AI API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_article(article: ArticleRequest):
    """
    Analyze an article for credibility, bias, and coverage.

    Phase 2: Basic analysis with source credibility check
    Phase 3: Will add ML model integration
    """
    from services.analyzer import analyze_article_content

    result = await analyze_article_content(article)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
