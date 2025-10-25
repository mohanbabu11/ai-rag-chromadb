#!/usr/bin/env python3
"""
Log viewer for Customer Care Agent
"""
import os
import time
from pathlib import Path

def tail_log_file(log_file_path, lines=50):
    """Display the last N lines of a log file and follow new entries"""
    
    if not os.path.exists(log_file_path):
        print(f"❌ Log file not found: {log_file_path}")
        print("💡 Start the API server first to generate logs")
        return
    
    print(f"📋 Showing last {lines} lines from: {log_file_path}")
    print("=" * 80)
    
    # Show last N lines
    try:
        with open(log_file_path, 'r') as f:
            file_lines = f.readlines()
            recent_lines = file_lines[-lines:] if len(file_lines) > lines else file_lines
            
            for line in recent_lines:
                print(line.strip())
    except Exception as e:
        print(f"❌ Error reading log file: {e}")
        return
    
    print("=" * 80)
    print("📡 Following new log entries... (Press Ctrl+C to stop)")
    print()
    
    # Follow new entries
    try:
        with open(log_file_path, 'r') as f:
            # Go to end of file
            f.seek(0, 2)
            
            while True:
                line = f.readline()
                if line:
                    print(line.strip())
                else:
                    time.sleep(0.1)
                    
    except KeyboardInterrupt:
        print("\n🛑 Stopped following logs")
    except Exception as e:
        print(f"❌ Error following logs: {e}")

def main():
    """Main function"""
    print("📊 Customer Care Agent - Log Viewer")
    print("=" * 50)
    
    # Get log file path (same directory as API)
    current_dir = Path(__file__).parent
    log_file = current_dir / "customer_care_agent.log"
    
    print(f"🔍 Looking for log file: {log_file}")
    
    if not log_file.exists():
        print("❌ Log file not found!")
        print("💡 Tips:")
        print("   1. Make sure the API server is running")
        print("   2. The log file is created when the API starts")
        print("   3. Run: python3 src/customer-care-agent/api.py")
        return
    
    # Show file info
    stat = log_file.stat()
    print(f"📁 File size: {stat.st_size} bytes")
    print(f"📅 Last modified: {time.ctime(stat.st_mtime)}")
    print()
    
    # Start tailing
    tail_log_file(str(log_file))

if __name__ == "__main__":
    main()