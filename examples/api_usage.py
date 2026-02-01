#!/usr/bin/env python3
"""
Example script demonstrating the use of enhanced features.
This script shows how to interact with the CrawlX API.
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def example_api_endpoints():
    """Example: List all available endpoints."""
    print_section("Available API Endpoints")
    
    endpoints = [
        ("GET", "/", "API status"),
        ("GET", "/health", "Health check"),
        ("GET", "/items", "List items (supports ?tag=, ?limit=)"),
        ("GET", "/search", "Search items (supports ?q=, ?tag=, ?fuzzy=)"),
        ("GET", "/items/export", "Export as JSON"),
        ("GET", "/items/export/csv", "Export as CSV"),
        ("GET", "/items/export/pdf", "Export as PDF (supports ?style=, ?tag=, ?limit=)"),
        ("POST", "/scrape/run", "Trigger scraping (supports ?spiders=)"),
    ]
    
    print("\n{:<6} {:<30} {}".format("Method", "Endpoint", "Description"))
    print("-" * 80)
    for method, endpoint, description in endpoints:
        print("{:<6} {:<30} {}".format(method, endpoint, description))


def main():
    """Run examples."""
    print("\n" + "=" * 60)
    print(" CrawlX Enhanced Features - API Examples")
    print("=" * 60)
    print("\nNote: Make sure the API is running at http://localhost:8000")
    print("      Start it with: cd backend && uvicorn main:app --reload")
    
    try:
        # Check if API is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("\n✓ API is running and healthy")
            example_api_endpoints()
        else:
            print("\n✗ API is not responding correctly")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Cannot connect to API. Is it running?")
        print("   Start it with: cd backend && uvicorn main:app --reload")
        # Still show endpoints even if not running
        example_api_endpoints()
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
