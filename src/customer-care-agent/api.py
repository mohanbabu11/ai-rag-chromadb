import os
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from agent import CustomerCareAgent, CustomerQuery, CustomerResponse

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('customer_care_agent.log')  # Log file
    ]
)
logger = logging.getLogger(__name__)

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Look for .env file in parent directory
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from {env_path}")
        # Also try loading from current directory as backup
        load_dotenv()
    else:
        print("ℹ️  No .env file found in parent directory, trying current directory")
        load_dotenv()
except ImportError:
    print("ℹ️  python-dotenv not installed, using system environment variables")
    print("💡 Install with: pip install python-dotenv")

app = FastAPI(
    title="Customer Care Agent API",
    description="API for interacting with the Customer Care Agent",
    version="1.0.0"
)

agent: CustomerCareAgent = None

@app.on_event("startup")
async def startup_event():
    global agent
    
    logger.info("🚀 Starting Customer Care Agent API...")
    
    # Debug environment loading
    env_path = Path(__file__).parent.parent.parent / '.env'
    logger.info(f"🔍 Environment file path: {env_path}")
    logger.info(f"🔍 Environment file exists: {env_path.exists()}")
    
    google_env_vars = [k for k in os.environ.keys() if 'GOOGLE' in k]
    logger.info(f"🔍 Google environment variables found: {google_env_vars}")
    
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if api_key:
        logger.info(f"🔑 API Key loaded successfully (length: {len(api_key)} chars)")
        logger.debug(f"🔑 API Key preview: {api_key[:20]}...")
    else:
        logger.error("🔑 No API Key found!")
    
    if not api_key:
        error_msg = """
        ❌ GOOGLE_GENAI_API_KEY environment variable not set!
        
        To fix this:
        1. Get your API key from: https://aistudio.google.com/app/apikey
        2. Set it as an environment variable:
           export GOOGLE_GENAI_API_KEY='your-api-key-here'
        3. Or add it to the .env file in your project root
        
        Then restart the application.
        """
        logger.error(error_msg)
        raise RuntimeError("GOOGLE_GENAI_API_KEY environment variable not set")
    
    logger.info("🤖 Initializing Customer Care Agent...")
    try:
        agent = CustomerCareAgent(api_key=api_key)
        logger.info("✅ Agent initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {e}")
        raise

@app.post("/api/query", response_model=CustomerResponse)
async def handle_customer_query(query: CustomerQuery):
    logger.info(f"📥 Received query: {query.query[:50]}..." if len(query.query) > 50 else f"📥 Received query: {query.query}")
    logger.info(f"🔗 Session ID: {query.session_id}")
    
    if agent is None:
        logger.error("❌ Agent is not available")
        raise HTTPException(status_code=503, detail="agent is not available")
    
    try:
        response = await agent.handle_query(query)
        logger.info(f"📤 Response generated successfully for session: {response.session_id}")
        logger.debug(f"📤 Response preview: {response.response[:100]}...")
        return response
    except Exception as e:
        logger.error(f"❌ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def start_server(host: str="0.0.0.0", port: int=8000):
    logger.info(f"🚀 Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server(host="0.0.0.0", port=8000)