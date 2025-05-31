"""
Configuration module for the Telegram bot.
Handles environment variables and bot settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for bot settings."""
    
    # Required Telegram Bot API credentials
    API_ID = 28966180
    API_HASH: str = os.getenv("TELEGRAM_API_HASH", "61685cb638a45b448ad485dbb38bfab4")
    BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "7457923910:AAH5rtrSRmTsm80RdDqkaqL0VrEd_GD2hnM")
    
    # Optional configuration
    SESSION_NAME: str = os.getenv("SESSION_NAME", "telegram_bot")
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    
    # Bot behavior settings
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "/")
    MAX_MESSAGE_LENGTH: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))
    
    # Rate limiting
    RATE_LIMIT_MESSAGES: int = int(os.getenv("RATE_LIMIT_MESSAGES", "20"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
    
    # Admin settings
    ADMIN_IDS: list = [
        int(user_id.strip()) 
        for user_id in os.getenv("ADMIN_IDS", "6436992668").split(",") 
        if user_id.strip().isdigit()
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration parameters."""
        required_fields = ["API_ID", "API_HASH", "BOT_TOKEN"]
        missing_fields = []
        
        for field in required_fields:
            value = getattr(cls, field)
            if not value:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_fields)}\n"
                f"Please check your .env file or environment variables."
            )
        
        # Validate API_ID is numeric
        try:
            int(cls.API_ID)
        except ValueError:
            raise ValueError(
                f"TELEGRAM_API_ID must be a number, got: {cls.API_ID}\n"
                f"Please check that API_ID and API_HASH are not swapped."
            )
        
        # Validate API_HASH is a string (not numeric)
        if cls.API_HASH.isdigit():
            raise ValueError(
                f"TELEGRAM_API_HASH should be a hexadecimal string, got numeric value: {cls.API_HASH}\n"
                f"Please check that API_ID and API_HASH are not swapped."
            )
        
        return True
    
    @classmethod
    def get_pyrogram_config(cls) -> dict:
        """Get configuration dictionary for Pyrogram client."""
        cls.validate()
        
        return {
            "api_id": int(cls.API_ID),
            "api_hash": cls.API_HASH,
            "bot_token": cls.BOT_TOKEN,
            "workers": cls.WORKERS,
        }

# Create a global config instance
config = Config()
