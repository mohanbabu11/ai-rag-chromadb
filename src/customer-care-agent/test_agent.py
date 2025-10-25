#!/usr/bin/env python3
"""
Test script for the Customer Care Agent
"""
import os
import asyncio
from agent import CustomerCareAgent, CustomerQuery

async def test_agent():
    """Test the customer care agent with sample queries"""
    
    # Check for API key
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_GENAI_API_KEY environment variable not set")
        print("Please set it with: export GOOGLE_GENAI_API_KEY='your-api-key'")
        return
    
    print("🤖 Initializing Customer Care Agent...")
    
    try:
        # Initialize agent
        agent = CustomerCareAgent(api_key=api_key)
        print("✅ Agent initialized successfully!")
        
        # Test queries
        test_queries = [
            "What is your return policy?",
            "How can I track my order?",
            "What payment methods do you accept?",
            "Hello, how are you today?",
            "What are your customer support hours?"
        ]
        
        session_id = "test-session-123"
        
        for i, query_text in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {query_text}")
            print("-" * 60)
            
            # Create query
            query = CustomerQuery(
                query=query_text,
                session_id=session_id
            )
            
            # Get response
            response = await agent.handle_query(query)
            
            # Display results
            print(f"🤖 Response: {response.response}")
            print(f"📊 Confidence: {response.confidence_score:.2f}")
            print(f"📚 Used Knowledge Base: {response.sources_used}")
            print(f"🔗 Session ID: {response.session_id}")
            
        # Show session history
        print(f"\n📜 Session History for {session_id}:")
        print("-" * 60)
        history = agent.get_session_history(session_id)
        for entry in history:
            role_emoji = "👤" if entry["role"] == "user" else "🤖"
            print(f"{role_emoji} {entry['role'].title()}: {entry['content']}")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting Customer Care Agent Test")
    print("=" * 60)
    asyncio.run(test_agent())