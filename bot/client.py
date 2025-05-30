"""
Telegram bot client implementation using Pyrogram.
Handles bot initialization, plugin loading, and event handling.
"""

import asyncio
from typing import Dict, List
from pyrogram import Client, idle
from pyrogram.types import User
from bot.config import config
from bot.utils.logger import setup_logger
from bot.handlers import register_handlers

logger = setup_logger(__name__)

class TelegramBot:
    """Main Telegram bot client class."""
    
    def __init__(self):
        """Initialize the Telegram bot."""
        self.client = None
        self.bot_info: User = None
        self.is_running = False
        self.user_sessions: Dict[int, dict] = {}
        
        # Initialize Pyrogram client
        try:
            pyrogram_config = config.get_pyrogram_config()
            self.client = Client(
                name=config.SESSION_NAME,
                **pyrogram_config
            )
            logger.info("Pyrogram client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Pyrogram client: {e}")
            raise
    
    async def start(self):
        """Start the bot and register handlers."""
        try:
            # Start the Pyrogram client
            await self.client.start()
            self.is_running = True
            
            # Get bot information
            self.bot_info = await self.client.get_me()
            logger.info(f"Bot started: @{self.bot_info.username} ({self.bot_info.first_name})")
            
            # Register all handlers
            register_handlers(self.client)
            logger.info("All handlers registered successfully")
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot gracefully."""
        try:
            if self.client and self.is_running:
                await self.client.stop()
                self.is_running = False
                logger.info("Bot stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
    
    async def idle(self):
        """Keep the bot running until stopped."""
        if self.client and self.is_running:
            await idle()
    
    def track_user(self, user_id: int, data: dict = None):
        """Track user interaction for analytics."""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "first_seen": asyncio.get_event_loop().time(),
                "last_activity": asyncio.get_event_loop().time(),
                "message_count": 0,
                "commands_used": []
            }
        
        session = self.user_sessions[user_id]
        session["last_activity"] = asyncio.get_event_loop().time()
        session["message_count"] += 1
        
        if data:
            session.update(data)
    
    def get_user_stats(self, user_id: int) -> dict:
        """Get user interaction statistics."""
        return self.user_sessions.get(user_id, {})
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin."""
        return user_id in config.ADMIN_IDS
    
    async def send_to_admins(self, message: str):
        """Send a message to all admin users."""
        for admin_id in config.ADMIN_IDS:
            try:
                await self.client.send_message(admin_id, message)
            except Exception as e:
                logger.error(f"Failed to send message to admin {admin_id}: {e}")
