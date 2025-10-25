#!/usr/bin/env python3
"""
Environment setup and validation script for Customer Care Agent
"""
import os
import sys

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    
    # Check for API key
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    if not api_key:
        print("❌ GOOGLE_GENAI_API_KEY environment variable not set")
        print("   Please set it with: export GOOGLE_GENAI_API_KEY='your-api-key'")
        return False
    else:
        print(f"✅ GOOGLE_GENAI_API_KEY is set (length: {len(api_key)} characters)")
    
    # Check required packages
    required_packages = [
        "langchain",
        "langchain_community", 
        "langchain_google_genai",
        "langgraph",
        "chromadb",
        "fastapi",
        "uvicorn",
        "pydantic"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 To install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_sample_env_file():
    """Create a sample .env file"""
    env_content = """# Customer Care Agent Environment Variables

# Google Generative AI API Key (required)
# Get your API key from: https://aistudio.google.com/app/apikey
GOOGLE_GENAI_API_KEY=your-api-key-here

# Optional: Model configuration
GENAI_MODEL=gemini-2.0-flash

# Optional: Server configuration
HOST=0.0.0.0
PORT=3000

# Optional: Database configuration
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION_NAME=knowledge_case
"""
    
    env_file = ".env"
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"📄 Created sample {env_file} file")
        print("   Please edit it and add your API key")
    else:
        print(f"📄 {env_file} file already exists")

if __name__ == "__main__":
    print("🚀 Customer Care Agent - Environment Setup")
    print("=" * 60)
    
    # Create sample .env file
    setup_sample_env_file()
    
    print()
    
    # Check environment
    if check_environment():
        print("\n✅ Environment is properly set up!")
        print("🎉 You can now run the Customer Care Agent")
        print("\nNext steps:")
        print("1. Run tests: python test_agent.py")
        print("2. Start API server: python api.py")
    else:
        print("\n❌ Environment setup incomplete")
        print("Please fix the issues above before proceeding")