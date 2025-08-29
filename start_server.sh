#!/bin/bash

# Wikipedia Scraper API - Startup Script
# This script starts the FastAPI server with proper configuration

echo "🚀 Starting Wikipedia Scraper API..."
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.8+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if dependencies are installed
if ! python3 -c "import fastapi, uvicorn, requests, bs4" 2>/dev/null; then
    echo "📥 Installing missing dependencies..."
    pip install -r requirements.txt
fi

echo "🌐 Starting server on http://localhost:8000"
echo "📖 API documentation will be available at:"
echo "   • Interactive docs: http://localhost:8000/docs"
echo "   • ReDoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Start the server
python3 main.py
