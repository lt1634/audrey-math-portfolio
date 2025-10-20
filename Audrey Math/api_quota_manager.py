#!/usr/bin/env python3
"""
API Quota Manager for Audrey Math Course Generator
Controls API usage to prevent exceeding limits and unexpected costs.
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

class APIQuotaManager:
    """Manages API usage quotas and limits"""
    
    def __init__(self, quota_file: str = "api_quota.json"):
        self.quota_file = quota_file
        self.quotas = self._load_quotas()
        
        # Default quotas (can be overridden)
        self.default_quotas = {
            "daily_requests": 100,      # Max requests per day
            "hourly_requests": 20,      # Max requests per hour
            "daily_characters": 50000,  # Max characters per day
            "hourly_characters": 5000,  # Max characters per hour
            "minute_delay": 2,          # Delay between requests (seconds)
        }
        
        # Apply default quotas if not set
        for key, value in self.default_quotas.items():
            if key not in self.quotas:
                self.quotas[key] = value
    
    def _load_quotas(self) -> Dict:
        """Load quota settings from file"""
        if os.path.exists(self.quota_file):
            try:
                with open(self.quota_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_quotas(self):
        """Save quota settings to file"""
        with open(self.quota_file, 'w') as f:
            json.dump(self.quotas, f, indent=2)
    
    def _get_today_key(self, prefix: str) -> str:
        """Get today's date key for tracking"""
        today = datetime.now().strftime("%Y-%m-%d")
        return f"{prefix}_{today}"
    
    def _get_hour_key(self, prefix: str) -> str:
        """Get current hour key for tracking"""
        hour = datetime.now().strftime("%Y-%m-%d-%H")
        return f"{prefix}_{hour}"
    
    def check_request_quota(self) -> bool:
        """Check if we can make another request"""
        daily_key = self._get_today_key("daily_requests")
        hourly_key = self._get_hour_key("hourly_requests")
        
        daily_count = self.quotas.get(daily_key, 0)
        hourly_count = self.quotas.get(hourly_key, 0)
        
        daily_limit = self.quotas.get("daily_requests", 100)
        hourly_limit = self.quotas.get("hourly_requests", 20)
        
        if daily_count >= daily_limit:
            print(f"❌ Daily request quota exceeded ({daily_count}/{daily_limit})")
            return False
        
        if hourly_count >= hourly_limit:
            print(f"❌ Hourly request quota exceeded ({hourly_count}/{hourly_limit})")
            return False
        
        return True
    
    def check_character_quota(self, characters: int) -> bool:
        """Check if we can use this many characters"""
        daily_key = self._get_today_key("daily_characters")
        hourly_key = self._get_hour_key("hourly_characters")
        
        daily_count = self.quotas.get(daily_key, 0)
        hourly_count = self.quotas.get(hourly_key, 0)
        
        daily_limit = self.quotas.get("daily_characters", 50000)
        hourly_limit = self.quotas.get("hourly_characters", 5000)
        
        if daily_count + characters > daily_limit:
            print(f"❌ Daily character quota would be exceeded ({daily_count + characters}/{daily_limit})")
            return False
        
        if hourly_count + characters > hourly_limit:
            print(f"❌ Hourly character quota would be exceeded ({hourly_count + characters}/{hourly_limit})")
            return False
        
        return True
    
    def record_request(self, characters: int = 0):
        """Record a request and character usage"""
        daily_req_key = self._get_today_key("daily_requests")
        hourly_req_key = self._get_hour_key("hourly_requests")
        daily_char_key = self._get_today_key("daily_characters")
        hourly_char_key = self._get_hour_key("hourly_characters")
        
        # Increment counters
        self.quotas[daily_req_key] = self.quotas.get(daily_req_key, 0) + 1
        self.quotas[hourly_req_key] = self.quotas.get(hourly_req_key, 0) + 1
        
        if characters > 0:
            self.quotas[daily_char_key] = self.quotas.get(daily_char_key, 0) + characters
            self.quotas[hourly_char_key] = self.quotas.get(hourly_char_key, 0) + characters
        
        self._save_quotas()
    
    def wait_if_needed(self):
        """Wait between requests if needed"""
        minute_delay = self.quotas.get("minute_delay", 2)
        if minute_delay > 0:
            print(f"⏳ Waiting {minute_delay} seconds between requests...")
            time.sleep(minute_delay)
    
    def get_usage_stats(self) -> Dict:
        """Get current usage statistics"""
        daily_req_key = self._get_today_key("daily_requests")
        hourly_req_key = self._get_hour_key("hourly_requests")
        daily_char_key = self._get_today_key("daily_characters")
        hourly_char_key = self._get_hour_key("hourly_characters")
        
        return {
            "daily_requests": self.quotas.get(daily_req_key, 0),
            "daily_requests_limit": self.quotas.get("daily_requests", 100),
            "hourly_requests": self.quotas.get(hourly_req_key, 0),
            "hourly_requests_limit": self.quotas.get("hourly_requests", 20),
            "daily_characters": self.quotas.get(daily_char_key, 0),
            "daily_characters_limit": self.quotas.get("daily_characters", 50000),
            "hourly_characters": self.quotas.get(hourly_char_key, 0),
            "hourly_characters_limit": self.quotas.get("hourly_characters", 5000),
        }
    
    def print_usage_stats(self):
        """Print current usage statistics"""
        stats = self.get_usage_stats()
        print("\n📊 API Usage Statistics:")
        print(f"Daily Requests: {stats['daily_requests']}/{stats['daily_requests_limit']}")
        print(f"Hourly Requests: {stats['hourly_requests']}/{stats['hourly_requests_limit']}")
        print(f"Daily Characters: {stats['daily_characters']:,}/{stats['daily_characters_limit']:,}")
        print(f"Hourly Characters: {stats['hourly_characters']:,}/{stats['hourly_characters_limit']:,}")
    
    def reset_daily_quotas(self):
        """Reset daily quotas (call this daily)"""
        today = datetime.now().strftime("%Y-%m-%d")
        keys_to_remove = [key for key in self.quotas.keys() if not key.endswith(today)]
        for key in keys_to_remove:
            if key.startswith(("daily_requests_", "daily_characters_")):
                del self.quotas[key]
        self._save_quotas()
        print("✅ Daily quotas reset")

# Example usage
if __name__ == "__main__":
    quota_manager = APIQuotaManager()
    
    # Check if we can make a request
    if quota_manager.check_request_quota():
        print("✅ Can make API request")
        
        # Check character quota for a 1000 character request
        if quota_manager.check_character_quota(1000):
            print("✅ Character quota OK")
            
            # Record the request
            quota_manager.record_request(1000)
            quota_manager.print_usage_stats()
        else:
            print("❌ Character quota exceeded")
    else:
        print("❌ Request quota exceeded")
