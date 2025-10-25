# Customer Care Agent API - Request Body Examples

## 1. Basic Query (Minimum Required)
```json
{
  "query": "What is your return policy?"
}
```

## 2. Query with Session ID
```json
{
  "query": "How can I track my order?",
  "session_id": "user-session-123"
}
```

## 3. Complete Query with All Fields
```json
{
  "query": "What payment methods do you accept?",
  "session_id": "user-session-456",
  "customer_id": "customer-789"
}
```

## 4. Greeting/General Query
```json
{
  "query": "Hello, I need help with my account",
  "session_id": "session-abc123"
}
```

## 5. Specific Policy Question
```json
{
  "query": "What are your customer support hours?",
  "session_id": "support-session-001",
  "customer_id": "premium-customer-42"
}
```

## cURL Examples

### Basic POST request:
```bash
curl -X POST "http://localhost:8000/api/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is your return policy?"}'
```

### POST request with session:
```bash
curl -X POST "http://localhost:8000/api/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "How can I track my order?",
       "session_id": "user-session-123"
     }'
```

### Complete POST request:
```bash
curl -X POST "http://localhost:8000/api/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What payment methods do you accept?",
       "session_id": "user-session-456",
       "customer_id": "customer-789"
     }'
```

## Python Examples

### Using requests library:
```python
import requests

# Basic request
response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "query": "What is your return policy?"
    }
)

# Request with session
response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "query": "How can I track my order?",
        "session_id": "user-session-123"
    }
)

print(response.json())
```

### Using httpx (async):
```python
import httpx
import asyncio

async def query_agent():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/query",
            json={
                "query": "What are your customer support hours?",
                "session_id": "async-session-001"
            }
        )
        return response.json()

# Run the async function
result = asyncio.run(query_agent())
print(result)
```

## JavaScript/Node.js Examples

### Using fetch:
```javascript
const response = await fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'What is your return policy?',
    session_id: 'js-session-123'
  })
});

const result = await response.json();
console.log(result);
```

### Using axios:
```javascript
const axios = require('axios');

const response = await axios.post('http://localhost:8000/api/query', {
  query: 'How can I track my order?',
  session_id: 'axios-session-456',
  customer_id: 'customer-123'
});

console.log(response.data);
```

## Expected Response Format

The API will return a response in this format:

```json
{
  "response": "Our return policy allows customers to return items within 30 days of purchase for a full refund. Items must be unused and in original packaging. To initiate a return, log into your account and select 'Return Items' from your order history.",
  "session_id": "user-session-123",
  "knowledge_base": true,
  "context_used": "[Source 1] Our return policy allows customers to return items within 30 days..."
}
```

## Field Descriptions

- **query** (required): The customer's question or request as a string
- **session_id** (optional): A unique identifier for the conversation session
- **customer_id** (optional): A unique identifier for the customer

## Error Responses

### 422 Unprocessable Entity (Invalid Request Body):
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "query"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

### 503 Service Unavailable (Agent Not Ready):
```json
{
  "detail": "agent is not available"
}
```

### 500 Internal Server Error:
```json
{
  "detail": "Error message describing what went wrong"
}
```