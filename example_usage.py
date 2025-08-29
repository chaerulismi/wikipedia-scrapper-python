#!/usr/bin/env python3
"""
Example usage of the Wikipedia Scraper API
"""

import requests
import json
from typing import Dict, Any

class WikipediaScraperClient:
    """Client class for interacting with the Wikipedia Scraper API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Wikipedia-Scraper-Client/1.0'
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the API is healthy"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get API information"""
        response = self.session.get(f"{self.base_url}/")
        response.raise_for_status()
        return response.json()
    
    def scrape_page(self, url: str, include_metadata: bool = True, 
                   include_links: bool = False, include_images: bool = False) -> Dict[str, Any]:
        """Scrape a Wikipedia page"""
        data = {
            "url": url,
            "include_metadata": include_metadata,
            "include_links": include_links,
            "include_images": include_images
        }
        
        response = self.session.post(f"{self.base_url}/scrape", json=data)
        response.raise_for_status()
        return response.json()
    
    def scrape_multiple_pages(self, urls: list, **kwargs) -> list:
        """Scrape multiple Wikipedia pages"""
        results = []
        for url in urls:
            try:
                result = self.scrape_page(url, **kwargs)
                results.append(result)
                print(f"✅ Successfully scraped: {url}")
            except Exception as e:
                print(f"❌ Failed to scrape {url}: {e}")
                results.append({
                    "url": url,
                    "success": False,
                    "error": str(e)
                })
        return results

def main():
    """Main example function"""
    
    # Initialize the client
    client = WikipediaScraperClient()
    
    print("🌐 Wikipedia Scraper API - Example Usage")
    print("=" * 60)
    
    # Example 1: Basic health check
    print("\n1. Checking API health...")
    try:
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Service: {health['service']}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Example 2: Get API information
    print("\n2. Getting API information...")
    try:
        info = client.get_api_info()
        print(f"   Message: {info['message']}")
        print(f"   Version: {info['version']}")
        print(f"   Available endpoints: {list(info['endpoints'].keys())}")
    except Exception as e:
        print(f"   ❌ Failed to get API info: {e}")
    
    # Example 3: Scrape a single page
    print("\n3. Scraping a single Wikipedia page...")
    test_url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    
    try:
        result = client.scrape_page(
            url=test_url,
            include_metadata=True,
            include_links=True,
            include_images=False
        )
        
        if result['success']:
            print(f"   ✅ Successfully scraped: {result['title']}")
            print(f"   📄 Title: {result['title']}")
            print(f"   📝 Summary length: {len(result['summary'])} characters")
            print(f"   📖 Content length: {len(result['content'])} characters")
            
            if result['metadata']:
                print(f"   🌐 Language: {result['metadata'].get('language', 'Unknown')}")
                if result['metadata'].get('categories'):
                    print(f"   📂 Categories: {len(result['metadata']['categories'])} found")
            
            if result['links']:
                print(f"   🔗 Internal links: {len(result['links'])} found")
            
            # Show a preview of the summary
            summary_preview = result['summary'][:300] + "..." if len(result['summary']) > 300 else result['summary']
            print(f"\n   📋 Summary Preview:\n   {summary_preview}")
            
        else:
            print(f"   ❌ Scraping failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"   ❌ Error during scraping: {e}")
    
    # Example 4: Scrape multiple pages
    print("\n4. Scraping multiple Wikipedia pages...")
    urls = [
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Deep_learning",
        "https://en.wikipedia.org/wiki/Neural_network"
    ]
    
    try:
        results = client.scrape_multiple_pages(
            urls,
            include_metadata=True,
            include_links=False,
            include_images=False
        )
        
        successful_scrapes = [r for r in results if r.get('success', False)]
        failed_scrapes = [r for r in results if not r.get('success', False)]
        
        print(f"   📊 Results Summary:")
        print(f"      ✅ Successful: {len(successful_scrapes)}")
        print(f"      ❌ Failed: {len(failed_scrapes)}")
        
        # Show titles of successful scrapes
        if successful_scrapes:
            print(f"   📚 Successfully scraped pages:")
            for result in successful_scrapes:
                print(f"      • {result['title']}")
                
    except Exception as e:
        print(f"   ❌ Error during batch scraping: {e}")
    
    # Example 5: Custom scraping options
    print("\n5. Custom scraping options...")
    try:
        # Minimal scraping (just content, no metadata/links)
        minimal_result = client.scrape_page(
            url="https://en.wikipedia.org/wiki/Python_(programming_language)",
            include_metadata=False,
            include_links=False,
            include_images=False
        )
        
        if minimal_result['success']:
            print(f"   ✅ Minimal scraping successful for: {minimal_result['title']}")
            print(f"   📖 Content length: {len(minimal_result['content'])} characters")
            print(f"   📝 Summary length: {len(minimal_result['summary'])} characters")
            
            # Show that metadata and links are not included
            print(f"   🔍 Metadata included: {minimal_result.get('metadata') is not None}")
            print(f"   🔗 Links included: {minimal_result.get('links') is not None}")
            
    except Exception as e:
        print(f"   ❌ Error during custom scraping: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Example usage completed!")
    print("\n💡 Tips:")
    print("   • Use the interactive API docs at http://localhost:8000/docs")
    print("   • Check the README.md for more examples and API details")
    print("   • The API supports various Wikipedia language versions")
    print("   • All responses include success status and error messages")

if __name__ == "__main__":
    main()
