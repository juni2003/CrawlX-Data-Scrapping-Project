"""
Test script for custom URL scraper
"""
import requests
import json

def test_custom_scraper():
    """Test the custom URL scraper endpoint"""
    
    url = "http://localhost:8000/scrape/url"
    
    payload = {
        "url": "https://books.toscrape.com",
        "extract_type": "auto",
        "wait_for": 2
    }
    
    print("🔄 Testing Custom URL Scraper...")
    print(f"   Target: {payload['url']}\n")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(f"\n📊 Results:")
            print(f"   - Success: {data.get('success')}")
            print(f"   - URL: {data.get('url')}")
            print(f"   - Title: {data.get('metadata', {}).get('title')}")
            print(f"   - Word Count: {data.get('metadata', {}).get('word_count')}")
            print(f"   - Content Length: {len(data.get('content', ''))}")
            print(f"   - Tables Found: {len(data.get('tables', []))}")
            print(f"   - Lists Found: {len(data.get('lists', []))}")
            
            if data.get('content'):
                print(f"\n📝 Content Preview (first 200 chars):")
                print(f"   {data['content'][:200]}...")
                
            return True
        else:
            print(f"❌ FAILED with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    test_custom_scraper()
