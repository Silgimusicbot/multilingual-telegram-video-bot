import asyncio
from typing import Dict, List
from pyrogram import Client, idle
from pyrogram.types import User
from bot.config import config
from bot.utils.logger import setup_logger
from bot.handlers import register_handlers

logger = setup_logger(__name__)

class TelegramBot:
        self.client = None
        self.bot_info: User = None
        self.is_running = False
        self.user_sessions: Dict[int, dict] = {}
        
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
        try:
            if self.client and self.is_running:
                await self.client.stop()
                self.is_running = False
                logger.info("Bot stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
    
    async def idle(self):
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
        return user_id in config.ADMIN_IDS
    
    async def send_to_admins(self, message: str):