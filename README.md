# Wikipedia Scraper Python API

A powerful and efficient Python-based web crawler API that extracts content from Wikipedia pages. Built with FastAPI for high performance and BeautifulSoup for robust HTML parsing.

## 🚀 Features

- **Fast & Efficient**: Built with FastAPI for high-performance API responses
- **Smart Content Extraction**: Intelligently extracts main content, summaries, and metadata
- **Flexible Options**: Choose what to extract (content, metadata, links, images)
- **Clean Text Processing**: Removes citations, edit links, and normalizes whitespace
- **Error Handling**: Comprehensive error handling with meaningful error messages
- **CORS Support**: Ready for web applications with built-in CORS middleware
- **Logging**: Detailed logging for debugging and monitoring
- **Input Validation**: Pydantic models for request validation

## 📋 Requirements

- Python 3.8+
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd wikipedia-scrapper-python
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Starting the API Server

1. **Run the server:**
   ```bash
   python main.py
   ```

2. **Or using uvicorn directly:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at `http://localhost:8000`

### API Endpoints

#### 1. **GET /** - API Information
Returns basic API information and available endpoints.

#### 2. **GET /health** - Health Check
Returns the health status of the API service.

#### 3. **POST /scrape** - Scrape Wikipedia Page
Main endpoint for scraping Wikipedia pages.

**Request Body:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "include_metadata": true,
  "include_links": false,
  "include_images": false
}
```

**Parameters:**
- `url` (required): Wikipedia URL to scrape
- `include_metadata` (optional): Include page metadata (default: true)
- `include_links` (optional): Include internal Wikipedia links (default: false)
- `include_images` (optional): Include image URLs (default: false)

**Response:**
```json
{
  "title": "Python (programming language)",
  "content": "Full page content...",
  "summary": "First few paragraphs...",
  "metadata": {
    "language": "en",
    "last_modified": "Last modified info",
    "page_id": "12345",
    "categories": ["Programming languages", "Python"]
  },
  "links": ["https://en.wikipedia.org/wiki/...", ...],
  "images": ["https://upload.wikimedia.org/...", ...],
  "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
  "success": true,
  "message": "Content extracted successfully"
}
```

## 🧪 Testing

Run the test script to verify the API functionality:

```bash
python test_api.py
```

**Note:** Make sure the API server is running before executing the test script.

## 📚 Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "include_metadata": true,
    "include_links": true
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/scrape"
data = {
    "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "include_metadata": True,
    "include_links": True
}

response = requests.post(url, json=data)
result = response.json()

print(f"Title: {result['title']}")
print(f"Summary: {result['summary'][:200]}...")
print(f"Content length: {len(result['content'])} characters")
```

### Using JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/scrape', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://en.wikipedia.org/wiki/Python_(programming_language)',
    include_metadata: true,
    include_links: true
  })
});

const result = await response.json();
console.log('Title:', result.title);
console.log('Summary:', result.summary);
```

## 🔧 Configuration

The API runs on port 8000 by default. You can modify this in `main.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Change port here
```

## 📖 API Documentation

Once the server is running, you can access:

- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

## 🚨 Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid Wikipedia URL or malformed request
- **500 Internal Server Error**: Failed to fetch or parse the page
- **Connection Timeout**: 30-second timeout for page requests

## 🔒 Security Features

- Input validation using Pydantic models
- URL format validation for Wikipedia domains
- Request timeout protection
- User-Agent headers to mimic legitimate browsers

## 🧹 Content Cleaning

The API automatically cleans extracted content:

- Removes citation references `[1]`, `[2]`, etc.
- Removes edit links `[edit]`
- Normalizes whitespace and line breaks
- Filters out navigation and script elements

## 📁 Project Structure

```
wikipedia-scrapper-python/
├── main.py              # Main FastAPI application
├── test_api.py          # Test script for the API
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the API documentation at `/docs`
2. Review the error logs in the console
3. Ensure the Wikipedia URL is valid and accessible
4. Verify all dependencies are installed correctly

## 🚀 Future Enhancements

- Rate limiting and request throttling
- Caching for frequently requested pages
- Support for other Wikimedia projects
- Advanced content filtering options
- Export to various formats (JSON, XML, Markdown)
- Batch processing for multiple URLs