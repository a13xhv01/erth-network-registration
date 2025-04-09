import json
import time
from pathlib import Path
from datetime import datetime
import threading

# Global variables to store analytics data
analytics_data = {
    "latest": {},
    "history": []
}

# File paths
ANALYTICS_DIR = Path(__file__).parent.parent / "data"
ANALYTICS_FILE = ANALYTICS_DIR / "analytics.json"

def init_analytics():
    """Initialize analytics by loading existing data or creating new structure"""
    global analytics_data
    
    # Create data directory if it doesn't exist
    ANALYTICS_DIR.mkdir(exist_ok=True)
    
    try:
        if ANALYTICS_FILE.exists():
            with open(ANALYTICS_FILE, 'r') as f:
                analytics_data = json.load(f)
            print(f"Loaded analytics data from {ANALYTICS_FILE}")
        else:
            # Initialize with empty structure
            analytics_data = {
                "latest": {
                    "registrations": 0,
                    "verifications": 0,
                    "rejections": 0,
                    "timestamp": int(time.time())
                },
                "history": []
            }
            save_analytics()
            print("Initialized new analytics data")
            
        # Start periodic snapshot thread
        snapshot_thread = threading.Thread(target=periodic_snapshot, daemon=True)
        snapshot_thread.start()
        
    except Exception as e:
        print(f"Error initializing analytics: {str(e)}")
        # Create default data if loading fails
        analytics_data = {
            "latest": {
                "registrations": 0,
                "verifications": 0,
                "rejections": 0,
                "timestamp": int(time.time())
            },
            "history": []
        }

def get_latest_data():
    """Get the latest analytics data"""
    return analytics_data["latest"]

def get_all_data():
    """Get all historical analytics data"""
    return analytics_data["history"]

def update_analytics(action_type):
    """
    Update analytics counters
    
    Args:
        action_type (str): Type of action - "registration", "verification", or "rejection"
    """
    global analytics_data
    
    if action_type == "registration":
        analytics_data["latest"]["registrations"] += 1
    elif action_type == "verification":
        analytics_data["latest"]["verifications"] += 1
    elif action_type == "rejection":
        analytics_data["latest"]["rejections"] += 1
    
    # Update timestamp
    analytics_data["latest"]["timestamp"] = int(time.time())
    
    # Save to file
    save_analytics()

def save_analytics():
    """Save analytics data to file"""
    try:
        with open(ANALYTICS_FILE, 'w') as f:
            json.dump(analytics_data, f, indent=2)
    except Exception as e:
        print(f"Error saving analytics data: {str(e)}")

def take_snapshot():
    """Take a snapshot of current analytics and add to history"""
    global analytics_data
    
    # Create a copy of latest data with current timestamp
    snapshot = analytics_data["latest"].copy()
    snapshot["timestamp"] = int(time.time())
    
    # Add to history
    analytics_data["history"].append(snapshot)
    
    # Limit history size (keep last 30 entries)
    if len(analytics_data["history"]) > 30:
        analytics_data["history"] = analytics_data["history"][-30:]
    
    # Save to file
    save_analytics()
    
    print(f"Analytics snapshot taken at {datetime.now().isoformat()}")

def periodic_snapshot(interval=3600):
    """Take periodic snapshots of analytics data"""
    while True:
        # Sleep for the specified interval
        time.sleep(interval)
        
        # Take a snapshot
        take_snapshot()