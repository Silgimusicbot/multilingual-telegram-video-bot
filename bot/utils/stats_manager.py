import json
import os
import requests
from datetime import datetime
from typing import Dict, Any

class StatsManager:
    """Manages bot statistics with persistent storage via GitHub Gist."""
    
    def __init__(self, gist_id: str = None):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.gist_id = gist_id
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict[str, Any]:
        """Load statistics from GitHub Gist."""
        if not self.github_token:
            print("GitHub token not found, using local storage")
            return self._get_default_stats()
        
        try:
            if self.gist_id:
                # Load from existing gist
                response = requests.get(
                    f"https://api.github.com/gists/{self.gist_id}",
                    headers={"Authorization": f"token {self.github_token}"}
                )
                if response.status_code == 200:
                    gist_data = response.json()
                    stats_content = gist_data["files"]["bot_stats.json"]["content"]
                    stats = json.loads(stats_content)
                    # Convert users list back to set
                    if "unique_users" in stats and isinstance(stats["unique_users"], list):
                        stats["unique_users"] = set(stats["unique_users"])
                    return stats
            
            # Try to find existing gist or create new one
            return self._find_or_create_gist()
            
        except Exception as e:
            print(f"Error loading stats from Gist: {e}")
            return self._get_default_stats()
    
    def _get_default_stats(self) -> Dict[str, Any]:
        """Get default stats structure."""
        return {
            "total_users": 0,
            "unique_users": set(),
            "total_downloads": 0,
            "platform_downloads": {
                "tiktok": 0,
                "instagram": 0,
                "youtube": 0
            },
            "commands_used": 0,
            "bot_started_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
    
    def _find_or_create_gist(self) -> Dict[str, Any]:
        """Find existing gist or create new one."""
        if not self.github_token:
            return self._get_default_stats()
        
        try:
            # Search for existing gist with bot statistics
            response = requests.get(
                "https://api.github.com/gists",
                headers={"Authorization": f"token {self.github_token}"}
            )
            
            if response.status_code == 200:
                gists = response.json()
                for gist in gists:
                    if "bot_stats.json" in gist.get("files", {}):
                        self.gist_id = gist["id"]
                        stats_content = gist["files"]["bot_stats.json"]["content"]
                        stats = json.loads(stats_content)
                        if "unique_users" in stats and isinstance(stats["unique_users"], list):
                            stats["unique_users"] = set(stats["unique_users"])
                        print(f"Found existing Gist: {self.gist_id}")
                        return stats
            
            # Create new gist if none found
            return self._create_new_gist()
            
        except Exception as e:
            print(f"Error finding/creating Gist: {e}")
            return self._get_default_stats()
    
    def _create_new_gist(self) -> Dict[str, Any]:
        """Create a new GitHub Gist for statistics."""
        if not self.github_token:
            return self._get_default_stats()
        
        default_stats = self._get_default_stats()
        
        try:
            gist_data = {
                "description": "Telegram Bot Statistics",
                "public": False,
                "files": {
                    "bot_stats.json": {
                        "content": json.dumps(self._prepare_stats_for_json(default_stats), indent=2)
                    }
                }
            }
            
            response = requests.post(
                "https://api.github.com/gists",
                headers={"Authorization": f"token {self.github_token}"},
                json=gist_data
            )
            
            if response.status_code == 201:
                gist_info = response.json()
                self.gist_id = gist_info["id"]
                print(f"Created new Gist for statistics: {self.gist_id}")
                return default_stats
                
        except Exception as e:
            print(f"Error creating Gist: {e}")
        
        return default_stats
    
    def _prepare_stats_for_json(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare stats for JSON serialization."""
        stats_copy = stats.copy()
        if isinstance(stats_copy.get("unique_users"), set):
            stats_copy["unique_users"] = list(stats_copy["unique_users"])
        return stats_copy
    
    def save_stats(self):
        """Save statistics to GitHub Gist."""
        if not self.github_token or not self.gist_id:
            return
        
        try:
            stats_for_json = self._prepare_stats_for_json(self.stats)
            
            gist_data = {
                "files": {
                    "bot_stats.json": {
                        "content": json.dumps(stats_for_json, indent=2, ensure_ascii=False)
                    }
                }
            }
            
            response = requests.patch(
                f"https://api.github.com/gists/{self.gist_id}",
                headers={"Authorization": f"token {self.github_token}"},
                json=gist_data
            )
            
            if response.status_code == 200:
                print("Statistics saved to Gist successfully")
            else:
                print(f"Error saving to Gist: {response.status_code}")
                
        except Exception as e:
            print(f"Error saving stats to Gist: {e}")
    
    def add_user(self, user_id: int):
        """Add a new user to statistics."""
        if isinstance(self.stats["unique_users"], list):
            self.stats["unique_users"] = set(self.stats["unique_users"])
        
        if user_id not in self.stats["unique_users"]:
            self.stats["unique_users"].add(user_id)
            self.stats["total_users"] = len(self.stats["unique_users"])
            self.update_activity()
            self.save_stats()
    
    def add_download(self, platform: str):
        """Add a download to statistics."""
        platform = platform.lower()
        if platform in self.stats["platform_downloads"]:
            self.stats["platform_downloads"][platform] += 1
            self.stats["total_downloads"] += 1
            self.update_activity()
            self.save_stats()
    
    def add_command(self):
        """Add a command usage to statistics."""
        self.stats["commands_used"] += 1
        self.update_activity()
        self.save_stats()
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.stats["last_activity"] = datetime.now().isoformat()
    
    def get_stats_text(self) -> str:
        """Get formatted statistics text."""
        if isinstance(self.stats["unique_users"], list):
            self.stats["unique_users"] = set(self.stats["unique_users"])
        
        started_date = datetime.fromisoformat(self.stats["bot_started_at"]).strftime("%d.%m.%Y")
        last_activity = datetime.fromisoformat(self.stats["last_activity"]).strftime("%d.%m.%Y %H:%M")
        
        return f"""📊 **Bot İstatistikləri**

👥 **İstifadəçilər:**
• Ümumi istifadəçi sayı: {len(self.stats["unique_users"])}
• İstifadə olunan əmrlər: {self.stats["commands_used"]}

📱 **Yüklənmiş Videolar:**
• Ümumi: {self.stats["total_downloads"]}
• TikTok: {self.stats["platform_downloads"]["tiktok"]}
• Instagram: {self.stats["platform_downloads"]["instagram"]}
• YouTube: {self.stats["platform_downloads"]["youtube"]}

🕐 **Tarixlər:**
• Bot başladılıb: {started_date}
• Son aktivlik: {last_activity}"""

# Global stats manager instance
stats_manager = StatsManager()
