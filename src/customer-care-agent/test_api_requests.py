#!/usr/bin/env python3
"""
Test script for Customer Care Agent API
"""
import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_request(query_data, description=""):
    """Test a single API request"""
    print(f"\n🧪 Testing: {description}")
    print(f"📤 Request: {json.dumps(query_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json=query_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"🤖 Response: {result.get('response', 'No response')}")
            print(f"🔗 Session ID: {result.get('session_id', 'None')}")
            print(f"📚 Used Knowledge Base: {result.get('knowledge_base', 'Unknown')}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the API server is running on localhost:3000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: The request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

def main():
    """Run API tests"""
    print("🚀 Customer Care Agent API Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"🏥 Health Check: {health_response.status_code}")
        if health_response.status_code != 200:
            print("⚠️  Server may not be ready")
    except:
        print("❌ Cannot connect to server. Make sure it's running with:")
        print("   python3 src/customer-care-agent/api.py")
        return
    
    # Test cases
    test_cases = [
        {
            "data": {
                "query": "What is your return policy?"
            },
            "description": "Basic policy question"
        },
        {
            "data": {
                "query": "How can I track my order?",
                "session_id": "test-session-001"
            },
            "description": "Order tracking with session"
        },
        {
            "data": {
                "query": "Hello, how are you today?",
                "session_id": "test-session-002",
                "customer_id": "customer-123"
            },
            "description": "General greeting (should not use knowledge base)"
        },
        {
            "data": {
                "query": "What payment methods do you accept?",
                "session_id": "test-session-003"
            },
            "description": "Payment methods question"
        },
        {
            "data": {
                "query": "What are your customer support hours?",
                "session_id": "test-session-004"
            },
            "description": "Support hours question"
        }
    ]
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        test_api_request(test_case["data"], f"{i}. {test_case['description']}")
        time.sleep(1)  # Small delay between requests
    
    print(f"\n🎉 Test suite completed!")
    print("\n💡 Tips:")
    print("- Check the server logs for detailed processing information")
    print("- Responses with knowledge_base=true used the knowledge base")
    print("- Session IDs allow for conversation continuity")

if __name__ == "__main__":
    main()