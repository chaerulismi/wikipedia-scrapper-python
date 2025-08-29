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
    
    # Test Wikipedia URL (Indonesian dishes page with tables)
    test_url = "https://en.wikipedia.org/wiki/List_of_Indonesian_dishes"
    
    # Test data
    test_data = {
        "url": test_url,
        "include_metadata": True,
        "include_links": True,
        "include_images": False,
        "include_tables": True
    }
    
    print("🚀 Testing Wikipedia Scraper API with Table Extraction")
    print("=" * 60)
    
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
    
    # Test 3: Wikipedia scraping with tables
    print("\n3. Testing Wikipedia scraping with table extraction...")
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
            
            # Test table extraction
            if result.get('tables'):
                print(f"📊 Tables Found: {len(result['tables'])}")
                for i, table in enumerate(result['tables']):
                    print(f"   Table {i+1}:")
                    if table.get('caption'):
                        print(f"     Caption: {table['caption']}")
                    if table.get('headers'):
                        print(f"     Headers: {len(table['headers'])} columns")
                        print(f"       {table['headers']}")
                    if table.get('rows'):
                        print(f"     Rows: {len(table['rows'])} data rows")
                        # Show first few rows as preview
                        for j, row in enumerate(table['rows'][:3]):
                            print(f"       Row {j+1}: {row[:3]}...")  # Show first 3 columns
                        if len(table['rows']) > 3:
                            print(f"       ... and {len(table['rows']) - 3} more rows")
            else:
                print("📊 No tables found on this page")
            
            # Show first 200 characters of summary
            summary_preview = result['summary'][:200] + "..." if len(result['summary']) > 200 else result['summary']
            print(f"\n📋 Summary Preview:\n{summary_preview}")
            
        else:
            print(f"❌ Wikipedia scraping failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Wikipedia scraping error: {e}")
    
    # Test 4: Test with minimal options but including tables
    print("\n4. Testing minimal scraping options with tables...")
    try:
        minimal_data = {
            "url": test_url,
            "include_metadata": False,
            "include_links": False,
            "include_images": False,
            "include_tables": True
        }
        
        response = requests.post(
            f"{base_url}/scrape",
            json=minimal_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Minimal scraping with tables successful!")
            result = response.json()
            print(f"   Content length: {len(result['content'])} characters")
            print(f"   Metadata included: {result['metadata'] is not None}")
            print(f"   Links included: {result['links'] is not None}")
            print(f"   Tables included: {result['tables'] is not None}")
            if result.get('tables'):
                print(f"   Number of tables: {len(result['tables'])}")
        else:
            print(f"❌ Minimal scraping failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Minimal scraping error: {e}")
    
    # Test 5: Test without tables
    print("\n5. Testing scraping without tables...")
    try:
        no_tables_data = {
            "url": test_url,
            "include_metadata": True,
            "include_links": False,
            "include_images": False,
            "include_tables": False
        }
        
        response = requests.post(
            f"{base_url}/scrape",
            json=no_tables_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Scraping without tables successful!")
            result = response.json()
            print(f"   Content length: {len(result['content'])} characters")
            print(f"   Tables included: {result['tables'] is not None}")
            if result.get('tables') is None:
                print("   ✅ Tables correctly excluded")
            else:
                print("   ❌ Tables should have been excluded")
        else:
            print(f"❌ Scraping without tables failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Scraping without tables error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Testing completed!")

if __name__ == "__main__":
    test_wikipedia_scraper()
