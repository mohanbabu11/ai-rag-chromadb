import os
import uuid
from typing import Dict, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from graph import CustomerCareAgentGraph, AgentState


class CustomerQuery(BaseModel):
    """Model for incoming customer queries"""
    query: str = Field(..., description="The customer's question or request")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation continuity")
    customer_id: Optional[str] = Field(None, description="Customer identifier")

class CustomerResponse(BaseModel):
    """Model for agent responses"""
    response: str = Field(..., description="The agent's response to the customer")
    session_id: str = Field(..., description="Session identifier")
    knowledge_base: Optional[bool] = Field(None, description="Whether knowledge base was consulted")
    context_used: Optional[str] = Field(None, description="Context retrieved from knowledge base")


class CustomerCareAgent:
    """Main Customer Care Agent that handles customer queries using LangGraph"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        """
        Initialize the Customer Care Agent
        
        Args:
            api_key (str): Google Generative AI API key
            model (str): Model name to use for generation
        """
        self.api_key = api_key
        print("API Key in agent py:", api_key)
        self.model = model
        self.graph = CustomerCareAgentGraph(api_key=api_key, model=model)
        self.sessions: Dict[str, list] = {}  # Store conversation history per session
        
    async def handle_query(self, query: CustomerQuery) -> CustomerResponse:
        """
        Handle a customer query and return a response
        
        Args:
            query (CustomerQuery): The customer's query
            
        Returns:
            CustomerResponse: The agent's response
        """
        # Generate session ID if not provided
        session_id = query.session_id or str(uuid.uuid4())

        # Initialize session if not exists
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        
        # Prepare initial state
        initial_state: AgentState = {
            "messages": [HumanMessage(content=query.query)],
            "query": query.query,
            "retrieved_context": "",
            "needs_knowledge": False,
            "response": "",
            "session_id": session_id
        }
        
        try:
            # Run the graph
            final_state = await self.graph.aprocess_query(query.query, session_id)
            
            # Extract response
            response_text = self._extract_response(final_state)
            
            # Store conversation in session
            self.sessions[session_id].extend([
                {"role": "user", "content": query.query},
                {"role": "assistant", "content": response_text}
            ])
            
            # Determine if knowledge base was used
            sources_used = final_state.get("needs_knowledge", False)
            
            return CustomerResponse(
                response=response_text,
                session_id=session_id,
                knowledge_base=sources_used,
                context_used=final_state.get("retrieved_context", "")
            )
            
        except Exception as e:
            # Return error response
            error_response = f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
            return CustomerResponse(
                response=error_response,
                session_id=session_id,
                knowledge_base=sources_used,
                context_used=final_state.get("retrieved_context", "")
            )
    
    async def _run_graph(self, initial_state: AgentState) -> AgentState:
        """
        Run the LangGraph workflow
        
        Args:
            initial_state (AgentState): Initial state for the graph
            
        Returns:
            AgentState: Final state after graph execution
        """
        # Since the graph might not be async, we'll run it synchronously
        # In a real implementation, you might want to use asyncio.run_in_executor
        result = self.graph.invoke(initial_state)
        return result
    
    def _extract_response(self, final_state: AgentState) -> str:
        """
        Extract the response text from the final state
        
        Args:
            final_state (AgentState): Final state from graph execution
            
        Returns:
            str: The response text
        """
        response = final_state.get("response", "")
        
        # If response is a message object, extract content
        if hasattr(response, 'content'):
            return response.content
        
        # If it's already a string, return as is
        if isinstance(response, str):
            return response
        
        # Fallback response
        return "I apologize, but I wasn't able to generate a proper response. Please try rephrasing your question."
    
    def _calculate_confidence(self, final_state: AgentState) -> float:
        """
        Calculate confidence score based on the agent's state
        
        Args:
            final_state (AgentState): Final state from graph execution
            
        Returns:
            float: Confidence score between 0 and 1
        """
        # Simple confidence calculation logic
        base_confidence = 0.7
        
        # Higher confidence if knowledge base was used and context was retrieved
        if final_state.get("needs_knowledge", False) and final_state.get("retrieved_context", ""):
            base_confidence += 0.2
        
        # Lower confidence if no response was generated
        if not final_state.get("response", ""):
            base_confidence -= 0.4
        
        return max(0.0, min(1.0, base_confidence))
    
    def get_session_history(self, session_id: str) -> list:
        """
        Get conversation history for a session
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            list: Conversation history
        """
        return self.sessions.get(session_id, [])
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear conversation history for a session
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            bool: True if session was cleared, False if session didn't exist
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_active_sessions(self) -> list:
        """
        Get list of active session IDs
        
        Returns:
            list: List of active session IDs
        """
        return list(self.sessions.keys())

# Utility function to create agent with environment variable
def create_agent_from_env() -> CustomerCareAgent:
    """
    Create a CustomerCareAgent using environment variables
    
    Returns:
        CustomerCareAgent: Initialized agent
        
    Raises:
        ValueError: If required environment variables are not set
    """
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_GENAI_API_KEY environment variable must be set")
    
    model = os.getenv("GENAI_MODEL", "gemini-2.0-flash")
    
    return CustomerCareAgent(api_key=api_key, model=model)

if __name__ == "__main__":
    # Test the agent
    import asyncio
    
    async def test_agent():
        # Create agent (make sure to set GOOGLE_GENAI_API_KEY environment variable)
        try:
            agent = create_agent_from_env()
            
            # Test query
            test_query = CustomerQuery(
                query="What is your return policy?",
                session_id="test-session-001"
            )
            
            response = await agent.handle_query(test_query)
            print(f"Query: {test_query.query}")
            print(f"Response: {response.response}")
            print(f"Session ID: {response.session_id}")
            print(f"Sources Used: {response.sources_used}")
            print(f"Confidence: {response.confidence_score}")
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Please set the GOOGLE_GENAI_API_KEY environment variable")
    
    # Run test
    asyncio.run(test_agent())
