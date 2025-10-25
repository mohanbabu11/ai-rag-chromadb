# Customer Care Agent

A sophisticated AI-powered customer care agent built with LangChain, LangGraph, and Google's Generative AI. The agent can handle customer queries by intelligently deciding whether to consult a knowledge base or provide direct responses.

## Features

- **Intelligent Query Classification**: Automatically determines if a query needs knowledge base lookup
- **RAG (Retrieval-Augmented Generation)**: Uses ChromaDB for efficient document retrieval
- **Conversation Memory**: Maintains session-based conversation history
- **RESTful API**: FastAPI-based API for easy integration
- **Flexible Architecture**: Built with LangGraph for complex workflow management

## Architecture

```
Customer Query → Agent → Graph Workflow
                         ├── Classify Query
                         ├── Retrieve Knowledge (if needed)
                         └── Generate Response
```

## Components

1. **`agent.py`**: Main CustomerCareAgent class with session management
2. **`graph.py`**: LangGraph workflow for query processing
3. **`knowledge_case.py`**: ChromaDB integration for knowledge retrieval
4. **`api.py`**: FastAPI REST API endpoints
5. **`test_agent.py`**: Test script for validation
6. **`setup_env.py`**: Environment setup and validation

## Setup

### 1. Prerequisites

- Python 3.8+
- Google Generative AI API key

### 2. Install Dependencies

```bash
# Install required packages
pip install langchain langchain-community langchain-google-genai langgraph chromadb fastapi uvicorn pydantic
```

### 3. Environment Setup

```bash
# Run the setup script
python setup_env.py

# Set your API key
export GOOGLE_GENAI_API_KEY='your-api-key-here'
```

### 4. Get API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Set it as an environment variable

## Usage

### Testing the Agent

```bash
# Run the test script
python test_agent.py
```

### Starting the API Server

```bash
# Start the FastAPI server
python api.py
```

The API will be available at `http://localhost:3000`

### API Endpoints

#### POST `/api/query`

Send a customer query to the agent.

**Request Body:**
```json
{
  "query": "What is your return policy?",
  "session_id": "optional-session-id",
  "customer_id": "optional-customer-id"
}
```

**Response:**
```json
{
  "response": "Our return policy allows customers to return items within 30 days...",
  "session_id": "session-123",
  "confidence_score": 0.9,
  "sources_used": true
}
```

### Using the Agent Programmatically

```python
import asyncio
from agent import CustomerCareAgent, CustomerQuery

async def example():
    # Initialize agent
    agent = CustomerCareAgent(api_key="your-api-key")
    
    # Create query
    query = CustomerQuery(
        query="How can I track my order?",
        session_id="my-session"
    )
    
    # Get response
    response = await agent.handle_query(query)
    print(response.response)

# Run example
asyncio.run(example())
```

## Knowledge Base

The system comes with a sample knowledge base containing information about:

- Return policies
- Shipping information
- Order tracking
- Payment methods
- Customer support hours

You can extend the knowledge base by adding more documents to the `KnowledgeCase.create_sample_knowledge_base()` method.

## Configuration

### Environment Variables

- `GOOGLE_GENAI_API_KEY`: Required. Your Google Generative AI API key
- `GENAI_MODEL`: Optional. Model to use (default: "gemini-2.0-flash")
- `HOST`: Optional. API server host (default: "0.0.0.0")
- `PORT`: Optional. API server port (default: 3000)
- `CHROMA_PERSIST_DIR`: Optional. ChromaDB persistence directory
- `CHROMA_COLLECTION_NAME`: Optional. ChromaDB collection name

### Model Configuration

You can customize the model settings in the `CustomerCareAgentGraph` class:

```python
self.llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Change model here
    temperature=0.2,           # Adjust creativity
    max_output_tokens=1024     # Adjust response length
)
```

## Workflow Details

1. **Classification**: The agent first determines if the query needs knowledge base lookup
2. **Retrieval**: If needed, relevant documents are retrieved from ChromaDB
3. **Generation**: A response is generated using the LLM, optionally incorporating retrieved context
4. **Response**: The final response is returned with metadata (confidence, sources used, etc.)

## Extending the System

### Adding New Knowledge

```python
from knowledge_case import KnowledgeCase
from langchain_core.documents import Document

# Create knowledge base
kc = KnowledgeCase(api_key="your-api-key")

# Add new documents
new_docs = [
    Document(
        page_content="Your new policy or information here",
        metadata={"source": "new_policy.txt"}
    )
]

kc.add_documents(new_docs)
```

### Customizing the Workflow

Modify the `_build_graph()` method in `CustomerCareAgentGraph` to add new nodes or change the workflow logic.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
2. **API Key Errors**: Verify your Google Generative AI API key is set correctly
3. **Model Errors**: Check if the specified model name is valid

### Running Diagnostics

```bash
# Check environment setup
python setup_env.py

# Run with debug output
python -v test_agent.py
```

## License

This project is open source and available under the MIT License.