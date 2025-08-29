from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
import re
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Wikipedia Scraper API",
    description="An API to scrape content from Wikipedia pages",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WikipediaRequest(BaseModel):
    url: HttpUrl
    include_metadata: Optional[bool] = True
    include_links: Optional[bool] = False
    include_images: Optional[bool] = False

class WikipediaResponse(BaseModel):
    title: str
    content: str
    summary: str
    metadata: Optional[dict] = None
    links: Optional[List[str]] = None
    images: Optional[List[str]] = None
    url: str
    success: bool
    message: str

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove citation references like [1], [2], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # Remove edit links like [edit]
    text = re.sub(r'\[edit\]', '', text)
    return text

def extract_wikipedia_content(url: str, include_metadata: bool = True, 
                           include_links: bool = False, include_images: bool = False) -> WikipediaResponse:
    """Extract content from a Wikipedia page"""
    
    try:
        # Validate Wikipedia URL
        if not re.match(r'https?://[a-z]+\.wikipedia\.org/wiki/', url):
            raise ValueError("Invalid Wikipedia URL format")
        
        # Set headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', {'id': 'firstHeading'})
        title = clean_text(title_elem.get_text()) if title_elem else "Unknown Title"
        
        # Extract main content
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            raise ValueError("Could not find content on the page")
        
        # Remove unwanted elements
        for unwanted in content_div.find_all(['script', 'style', 'sup', 'nav', 'table']):
            unwanted.decompose()
        
        # Extract paragraphs for main content
        paragraphs = content_div.find_all('p')
        content = '\n\n'.join([clean_text(p.get_text()) for p in paragraphs if p.get_text().strip()])
        
        # Extract summary (first few meaningful paragraphs)
        summary_paragraphs = []
        for p in paragraphs[:3]:  # First 3 paragraphs
            text = clean_text(p.get_text())
            if len(text) > 50:  # Only meaningful paragraphs
                summary_paragraphs.append(text)
        summary = '\n\n'.join(summary_paragraphs)
        
        # Extract metadata if requested
        metadata = None
        if include_metadata:
            metadata = {
                'language': soup.find('html', {}).get('lang', 'unknown'),
                'last_modified': None,
                'page_id': None,
                'categories': []
            }
            
            # Try to get last modified date
            last_modified = soup.find('div', {'id': 'footer-info-lastmod'})
            if last_modified:
                metadata['last_modified'] = clean_text(last_modified.get_text())
            
            # Try to get page ID
            page_id_elem = soup.find('meta', {'name': 'page_id'})
            if page_id_elem:
                metadata['page_id'] = page_id_elem.get('content')
            
            # Try to get categories
            category_links = soup.find_all('a', {'class': 'mw-category-link'})
            if category_links:
                metadata['categories'] = [clean_text(link.get_text()) for link in category_links]
        
        # Extract links if requested
        links = None
        if include_links:
            link_elements = content_div.find_all('a', href=True)
            links = []
            for link in link_elements:
                href = link.get('href')
                if href.startswith('/wiki/') and not href.startswith('/wiki/Special:'):
                    links.append(f"https://en.wikipedia.org{href}")
        
        # Extract images if requested
        images = None
        if include_images:
            img_elements = content_div.find_all('img')
            images = []
            for img in img_elements:
                src = img.get('src')
                if src and not src.startswith('data:'):
                    if src.startswith('//'):
                        images.append(f"https:{src}")
                    elif src.startswith('/'):
                        images.append(f"https://en.wikipedia.org{src}")
                    else:
                        images.append(src)
        
        return WikipediaResponse(
            title=title,
            content=content,
            summary=summary,
            metadata=metadata,
            links=links,
            images=images,
            url=url,
            success=True,
            message="Content extracted successfully"
        )
        
    except requests.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch the page: {str(e)}")
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Wikipedia Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "POST /scrape": "Scrape Wikipedia page content",
            "GET /health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Wikipedia Scraper API"}

@app.post("/scrape", response_model=WikipediaResponse)
async def scrape_wikipedia(request: WikipediaRequest):
    """
    Scrape content from a Wikipedia page
    
    - **url**: The Wikipedia URL to scrape
    - **include_metadata**: Whether to include page metadata (default: True)
    - **include_links**: Whether to include internal Wikipedia links (default: False)
    - **include_images**: Whether to include image URLs (default: False)
    """
    logger.info(f"Scraping request received for URL: {request.url}")
    
    try:
        result = extract_wikipedia_content(
            str(request.url),
            include_metadata=request.include_metadata,
            include_links=request.include_links,
            include_images=request.include_images
        )
        logger.info(f"Successfully scraped content from: {request.url}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to scrape the Wikipedia page")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
