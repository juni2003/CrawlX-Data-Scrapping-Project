"""
Comprehensive test suite for Custom URL Scraper
Tests multiple URLs to verify the httpx-based scraper works correctly
"""
import requests
import json
from typing import Dict, Any

def test_url(url: str, expected_success: bool = True) -> Dict[str, Any]:
    """Test scraping a single URL"""
    
    api_url = "http://localhost:8000/scrape/url"
    payload = {
        "url": url,
        "extract_type": "auto",
        "wait_for": 2
    }
    
    print(f"\n{'='*60}")
    print(f"Testing: {url}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            result = {
                "url": url,
                "status": "✅ SUCCESS",
                "success": data.get('success'),
                "title": data.get('title'),
                "content_length": len(data.get('content', '')),
                "tables": len(data.get('tables', [])),
                "lists": len(data.get('lists', [])),
                "extracted_at": data.get('extracted_at')
            }
            
            print(f"Status: {result['status']}")
            print(f"Title: {result['title']}")
            print(f"Content: {result['content_length']} characters")
            print(f"Tables: {result['tables']}")
            print(f"Lists: {result['lists']}")
            
            if result['content_length'] > 0:
                preview = data['content'][:150].replace('\n', ' ')
                print(f"\nPreview: {preview}...")
            
            return result
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return {
                "url": url,
                "status": f"❌ FAILED: HTTP {response.status_code}",
                "error": response.text
            }
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend")
        print("Make sure backend is running on http://localhost:8000")
        return {
            "url": url,
            "status": "❌ ERROR: Connection failed",
            "error": "Backend not running"
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {
            "url": url,
            "status": f"❌ ERROR: {type(e).__name__}",
            "error": str(e)
        }

def run_test_suite():
    """Run comprehensive test suite"""
    
    print("\n" + "="*60)
    print("  CrawlX Custom URL Scraper - Test Suite")
    print("="*60)
    
    # Test URLs - mix of different content types
    test_cases = [
        # E-commerce (static)
        "https://books.toscrape.com",
        
        # Documentation (static)
        "https://httpx.readthedocs.io",
        
        # News/Blog (server-rendered)
        "https://example.com",
    ]
    
    results = []
    for url in test_cases:
        result = test_url(url)
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    
    successful = sum(1 for r in results if "SUCCESS" in r['status'])
    total = len(results)
    
    print(f"\nPassed: {successful}/{total}")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['url']}")
        print(f"   {result['status']}")
        if 'content_length' in result:
            print(f"   Content: {result['content_length']} chars")
    
    print("\n" + "="*60)
    
    if successful == total:
        print("🎉 All tests passed!")
    elif successful > 0:
        print(f"⚠️  {successful}/{total} tests passed")
    else:
        print("❌ All tests failed")
    
    print("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    run_test_suite()
