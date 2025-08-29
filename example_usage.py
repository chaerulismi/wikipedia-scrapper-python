#!/usr/bin/env python3
"""
Example usage of the Wikipedia Scraper API with table extraction
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
                   include_links: bool = False, include_images: bool = False,
                   include_tables: bool = True) -> Dict[str, Any]:
        """Scrape a Wikipedia page"""
        data = {
            "url": url,
            "include_metadata": include_metadata,
            "include_links": include_links,
            "include_images": include_images,
            "include_tables": include_tables
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

def print_table_summary(table_data: Dict[str, Any], table_index: int):
    """Print a summary of extracted table data"""
    print(f"   📊 Table {table_index + 1}:")
    
    if table_data.get('caption'):
        print(f"     📝 Caption: {table_data['caption']}")
    
    if table_data.get('headers'):
        print(f"     🏷️  Headers ({len(table_data['headers'])} columns):")
        for i, header in enumerate(table_data['headers']):
            print(f"       {i+1}. {header}")
    
    if table_data.get('rows'):
        print(f"     📋 Data Rows: {len(table_data['rows'])}")
        # Show first 3 rows as preview
        for i, row in enumerate(table_data['rows'][:3]):
            preview = " | ".join([str(cell)[:30] + "..." if len(str(cell)) > 30 else str(cell) for cell in row[:3]])
            print(f"       Row {i+1}: {preview}")
        
        if len(table_data['rows']) > 3:
            print(f"       ... and {len(table_data['rows']) - 3} more rows")

def main():
    """Main example function"""
    
    # Initialize the client
    client = WikipediaScraperClient()
    
    print("🌐 Wikipedia Scraper API - Example Usage with Table Extraction")
    print("=" * 70)
    
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
    
    # Example 3: Scrape Indonesian dishes page with tables
    print("\n3. Scraping Indonesian dishes page with table extraction...")
    test_url = "https://en.wikipedia.org/wiki/List_of_Indonesian_dishes"
    
    try:
        result = client.scrape_page(
            url=test_url,
            include_metadata=True,
            include_links=True,
            include_images=False,
            include_tables=True
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
            
            # Show table extraction results
            if result.get('tables'):
                print(f"\n   📊 Table Extraction Results:")
                print(f"   Found {len(result['tables'])} tables on the page")
                
                for i, table in enumerate(result['tables']):
                    print_table_summary(table, i)
                    print()  # Empty line between tables
            else:
                print(f"   📊 No tables found on this page")
            
            # Show a preview of the summary
            summary_preview = result['summary'][:300] + "..." if len(result['summary']) > 300 else result['summary']
            print(f"\n   📋 Summary Preview:\n   {summary_preview}")
            
        else:
            print(f"   ❌ Scraping failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"   ❌ Error during scraping: {e}")
    
    # Example 4: Scrape multiple pages with tables
    print("\n4. Scraping multiple Wikipedia pages with table extraction...")
    urls = [
        "https://en.wikipedia.org/wiki/List_of_Indonesian_dishes",
        "https://en.wikipedia.org/wiki/List_of_Japanese_dishes",
        "https://en.wikipedia.org/wiki/List_of_Chinese_dishes"
    ]
    
    try:
        results = client.scrape_multiple_pages(
            urls,
            include_metadata=True,
            include_links=False,
            include_images=False,
            include_tables=True
        )
        
        successful_scrapes = [r for r in results if r.get('success', False)]
        failed_scrapes = [r for r in results if not r.get('success', False)]
        
        print(f"   📊 Results Summary:")
        print(f"      ✅ Successful: {len(successful_scrapes)}")
        print(f"      ❌ Failed: {len(failed_scrapes)}")
        
        # Show titles and table counts of successful scrapes
        if successful_scrapes:
            print(f"   📚 Successfully scraped pages with tables:")
            for result in successful_scrapes:
                table_count = len(result.get('tables', []))
                print(f"      • {result['title']} - {table_count} tables")
                
    except Exception as e:
        print(f"   ❌ Error during batch scraping: {e}")
    
    # Example 5: Custom scraping options - tables only
    print("\n5. Custom scraping - tables only...")
    try:
        # Scrape only tables, minimal other content
        tables_only_result = client.scrape_page(
            url="https://en.wikipedia.org/wiki/List_of_Indonesian_dishes",
            include_metadata=False,
            include_links=False,
            include_images=False,
            include_tables=True
        )
        
        if tables_only_result['success']:
            print(f"   ✅ Tables-only scraping successful for: {tables_only_result['title']}")
            print(f"   📖 Content length: {len(tables_only_result['content'])} characters")
            print(f"   📝 Summary length: {len(tables_only_result['summary'])} characters")
            
            # Show that metadata and links are not included
            print(f"   🔍 Metadata included: {tables_only_result.get('metadata') is not None}")
            print(f"   🔗 Links included: {tables_only_result.get('links') is not None}")
            print(f"   📊 Tables included: {tables_only_result.get('tables') is not None}")
            
            if tables_only_result.get('tables'):
                print(f"   📋 Table count: {len(tables_only_result['tables'])}")
                
    except Exception as e:
        print(f"   ❌ Error during tables-only scraping: {e}")
    
    # Example 6: Test without tables
    print("\n6. Testing scraping without tables...")
    try:
        no_tables_result = client.scrape_page(
            url="https://en.wikipedia.org/wiki/List_of_Indonesian_dishes",
            include_metadata=True,
            include_links=False,
            include_images=False,
            include_tables=False
        )
        
        if no_tables_result['success']:
            print(f"   ✅ Scraping without tables successful!")
            print(f"   📖 Content length: {len(no_tables_result['content'])} characters")
            print(f"   📊 Tables included: {no_tables_result.get('tables') is not None}")
            if no_tables_result.get('tables') is None:
                print("   ✅ Tables correctly excluded")
            else:
                print("   ❌ Tables should have been excluded")
                
    except Exception as e:
        print(f"   ❌ Error during no-tables scraping: {e}")
    
    print("\n" + "=" * 70)
    print("🏁 Example usage completed!")
    print("\n💡 Tips:")
    print("   • Use the interactive API docs at http://localhost:8000/docs")
    print("   • The API now supports table extraction with the include_tables parameter")
    print("   • Tables are extracted with headers, rows, and captions")
    print("   • Perfect for scraping structured data from Wikipedia list pages")
    print("   • Check the README.md for more examples and API details")

if __name__ == "__main__":
    main()
