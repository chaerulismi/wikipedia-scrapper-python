#!/usr/bin/env python3
"""
Test script for the Wikipedia Scraper API
"""

import requests
import json
from typing import Dict, Any

def test_wikipedia_scraper():
    """Test the Wikipedia scraper API with a sample Wikipedia page"""
    
    # API endpoint
    base_url = "http://localhost:8000"
    
    # Test Wikipedia URL (Python programming language page)
    test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    # Test data
    test_data = {
        "url": test_url,
        "include_metadata": True,
        "include_links": True,
        "include_images": False
    }
    
    print("🚀 Testing Wikipedia Scraper API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running!")
        return
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   API Info: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: Wikipedia scraping
    print("\n3. Testing Wikipedia scraping...")
    try:
        response = requests.post(
            f"{base_url}/scrape",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Wikipedia scraping successful!")
            result = response.json()
            
            print(f"\n📄 Page Title: {result['title']}")
            print(f"🔗 URL: {result['url']}")
            print(f"📝 Summary Length: {len(result['summary'])} characters")
            print(f"📖 Content Length: {len(result['content'])} characters")
            
            if result['metadata']:
                print(f"🌐 Language: {result['metadata'].get('language', 'Unknown')}")
                if result['metadata'].get('categories'):
                    print(f"📂 Categories: {len(result['metadata']['categories'])} found")
            
            if result['links']:
                print(f"🔗 Internal Links: {len(result['links'])} found")
            
            # Show first 200 characters of summary
            summary_preview = result['summary'][:200] + "..." if len(result['summary']) > 200 else result['summary']
            print(f"\n📋 Summary Preview:\n{summary_preview}")
            
        else:
            print(f"❌ Wikipedia scraping failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Wikipedia scraping error: {e}")
    
    # Test 4: Test with minimal options
    print("\n4. Testing minimal scraping options...")
    try:
        minimal_data = {
            "url": test_url,
            "include_metadata": False,
            "include_links": False,
            "include_images": False
        }
        
        response = requests.post(
            f"{base_url}/scrape",
            json=minimal_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Minimal scraping successful!")
            result = response.json()
            print(f"   Content length: {len(result['content'])} characters")
            print(f"   Metadata included: {result['metadata'] is not None}")
            print(f"   Links included: {result['links'] is not None}")
        else:
            print(f"❌ Minimal scraping failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Minimal scraping error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")

if __name__ == "__main__":
    test_wikipedia_scraper()
