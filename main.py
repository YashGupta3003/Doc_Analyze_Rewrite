from fastapi import FastAPI
from pydantic import BaseModel
from content_fetcher import ContentFetcher
from analyzer import ContentAnalyzer
import os
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()


#FastAPI app
app = FastAPI(
    title="Documentation Analyzer",
    description="Documentation analysis agent",
    version="1.0.0"
)

content_fetcher = ContentFetcher()
# Get gemini API key from env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY required")

content_analyzer = ContentAnalyzer(GEMINI_API_KEY)

# validation pydantic models
class AnalyzeRequest(BaseModel):
    url: str
class AnalysisSection(BaseModel):
    assessment: str
    suggestions: list[str]
class AnalyzeResponse(BaseModel):
    url: str
    title: str
    word_count: int
    status: str
    message: str
    analysis: Dict[str, AnalysisSection] = None

# root
@app.get("/")
async def root():
    return {"message": "Documentation Analyzer API is running!"}

# analysis endpoint
@app.post("/analyze-documentation", response_model=AnalyzeResponse)
async def analyze_documentation(request: AnalyzeRequest):
    # fetching content
    fetch_result = content_fetcher.fetch_content(request.url)
    
    if not fetch_result["success"]:
        return AnalyzeResponse(
            url=request.url,
            title="Unknown",
            word_count=0,
            status="error",
            message=f"Failed to fetch content: {fetch_result['error']}"
        )
    
    content_data = fetch_result["data"]
    
    # analyze content
    analysis_result = content_analyzer.analyze_content(content_data, request.url)
    
    if not analysis_result["success"]:
        return AnalyzeResponse(
            url=request.url,
            title=content_data.get('title', 'Unknown'),
            word_count=content_data.get('word_count', 0),
            status="error",
            message=f"Analysis failed: {analysis_result['error']}"
        )
    
    # formatting the response
    analysis_data = analysis_result["analysis"]
    formatted_analysis = {}
    
    for key, value in analysis_data.items():
        formatted_analysis[key] = AnalysisSection(
            assessment=value.get("assessment", "No assessment available"),
            suggestions=value.get("suggestions", [])
        )
    
    return AnalyzeResponse(
        url=request.url,
        title=analysis_result["title"],
        word_count=analysis_result["word_count"],
        status="success",
        message="Analysis completed successfully",
        analysis=formatted_analysis
    )

# only for content fetching
@app.post("/fetch-content")
async def fetch_content_only(request: AnalyzeRequest):
    result = content_fetcher.fetch_content(request.url)
    return result

from style_rewriter import StyleRewriter

style_rewriter = StyleRewriter()

class RewriteStyleRequest(BaseModel):
    url: str

class RewriteStyleResponse(BaseModel):
    url: str
    title: str
    revised_content: str
    status: str
    message: str

@app.post("/rewrite-style", response_model=RewriteStyleResponse)
async def rewrite_style(request: RewriteStyleRequest):
    # fetching content
    fetch_result = content_fetcher.fetch_content(request.url)
    if not fetch_result["success"]:
        return RewriteStyleResponse(
            url=request.url,
            title="Unknown",
            revised_content="",
            status="error",
            message=f"Failed to fetch content: {fetch_result['error']}"
        )
    content_data = fetch_result["data"]

    # analyze content completely to also get style suggestions
    analysis_result = content_analyzer.analyze_content(content_data, request.url)
    if not analysis_result["success"]:
        return RewriteStyleResponse(
            url=request.url,
            title=content_data.get('title', 'Unknown'),
            revised_content="",
            status="error",
            message=f"Analysis failed: {analysis_result['error']}"
        )
    style_section = analysis_result["analysis"].get("style_guidelines", {})
    style_suggestions = style_section.get("suggestions", [])
    assessment = style_section.get("assessment", "")

    #rewrite content for style
    revised_content = style_rewriter.rewrite_for_style(
        original_content=content_data.get("content_text", ""),
        style_suggestions=style_suggestions,
        assessment=assessment
    )

    return RewriteStyleResponse(
        url=request.url,
        title=content_data.get("title", "Unknown"),
        revised_content=revised_content,
        status="success",
        message="style-guideline-based revision completed"
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)