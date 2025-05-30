import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
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
        
        try:
            int(cls.API_ID)
        except ValueError:
            raise ValueError(
                f"TELEGRAM_API_ID must be a number, got: {cls.API_ID}\n"
                f"Please check that API_ID and API_HASH are not swapped."
            )
        
        if cls.API_HASH.isdigit():
            raise ValueError(
                f"TELEGRAM_API_HASH should be a hexadecimal string, got numeric value: {cls.API_HASH}\n"
                f"Please check that API_ID and API_HASH are not swapped."
            )
        
        return True
    
    @classmethod
    def get_pyrogram_config(cls) -> dict: