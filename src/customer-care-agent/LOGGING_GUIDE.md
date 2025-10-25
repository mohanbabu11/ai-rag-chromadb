# Customer Care Agent - Logging Guide

## 📊 Where to Find Logs

### 1. **Terminal Output** (Real-time)
When you run the API server:
```bash
python3 src/customer-care-agent/api.py
```
All logs appear directly in your terminal window.

### 2. **Log File** (Persistent)
The application now also writes logs to a file:
- **Location**: `src/customer-care-agent/customer_care_agent.log`
- **Format**: Timestamped entries with log levels
- **Persistence**: Logs remain after stopping the server

### 3. **View Log File**
Use the log viewer script:
```bash
python3 src/customer-care-agent/view_logs.py
```

## 🔍 Log Levels

### INFO (General Information)
- Server startup/shutdown
- Request processing
- Successful operations

### ERROR (Errors)
- API key issues
- Processing failures
- System errors

### DEBUG (Detailed Information)
- Environment variable details
- Response previews
- Internal state information

## 📋 Common Log Messages

### **Startup Logs**
```
🚀 Starting Customer Care Agent API...
🔍 Environment file path: /path/to/.env
🔑 API Key loaded successfully (length: 39 chars)
🤖 Initializing Customer Care Agent...
✅ Agent initialized successfully!
```

### **Request Logs**
```
📥 Received query: What is your return policy?
🔗 Session ID: user-session-123
📤 Response generated successfully for session: user-session-123
```

### **Error Logs**
```
❌ GOOGLE_GENAI_API_KEY environment variable not set!
❌ Agent is not available
❌ Error processing query: [error details]
```

## 🛠️ Troubleshooting with Logs

### **API Key Issues**
Look for:
- `🔑 API Key loaded successfully` (good)
- `🔑 No API Key found!` (bad)
- `API key not valid` (invalid key)

### **Agent Initialization**
Look for:
- `✅ Agent initialized successfully!` (good)
- `❌ Failed to initialize agent:` (bad)

### **Request Processing**
Look for:
- `📥 Received query:` (request received)
- `📤 Response generated successfully` (success)
- `❌ Error processing query:` (failure)

## 🔧 Enabling More Detailed Logs

### Method 1: Environment Variable
```bash
export LOG_LEVEL=DEBUG
python3 src/customer-care-agent/api.py
```

### Method 2: Modify Code
In `api.py`, change:
```python
logging.basicConfig(level=logging.DEBUG)  # More detailed
```

## 📁 Log File Management

### View Recent Logs
```bash
tail -f src/customer-care-agent/customer_care_agent.log
```

### View Last 100 Lines
```bash
tail -n 100 src/customer-care-agent/customer_care_agent.log
```

### Search Logs
```bash
grep "ERROR" src/customer-care-agent/customer_care_agent.log
grep "🔑" src/customer-care-agent/customer_care_agent.log
```

### Clear Old Logs
```bash
> src/customer-care-agent/customer_care_agent.log
```

## 🔄 Real-time Log Monitoring

### Terminal 1: Run API
```bash
python3 src/customer-care-agent/api.py
```

### Terminal 2: Watch Logs
```bash
python3 src/customer-care-agent/view_logs.py
```

### Terminal 3: Test API
```bash
python3 src/customer-care-agent/test_api_requests.py
```

## 📈 Log Analysis

### Count Request Types
```bash
grep -c "📥 Received query" customer_care_agent.log
```

### Find Errors
```bash
grep "❌" customer_care_agent.log
```

### Track Sessions
```bash
grep "🔗 Session ID" customer_care_agent.log
```

## 🚨 Important Log Locations

1. **API Server Logs**: Terminal + `customer_care_agent.log`
2. **System Logs**: Check your system's log directory
3. **Error Logs**: Look for `❌` symbols in logs
4. **Debug Info**: API key loading, environment checks

## 💡 Tips

- **Always check logs first** when troubleshooting
- **Use grep/search** to find specific issues quickly
- **Monitor logs in real-time** during testing
- **Keep logs** for debugging historical issues
- **Check both terminal and log file** for complete picture