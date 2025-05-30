"""
Handlers package for the Telegram bot.
Contains all message and command handlers.
"""

from pyrogram import Client
from .commands import register_command_handlers
from .messages import register_message_handlers
from bot.plugins import load_all_plugins
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def register_handlers(client: Client):
    """Register all bot handlers."""
    try:
        # Register command handlers first
        register_command_handlers(client)
        logger.info("Command handlers registered")
        
        # Load plugins before message handlers so they get priority
        load_all_plugins(client)
        logger.info("All plugins loaded")
        
        # Register general message handlers last
        register_message_handlers(client)
        logger.info("Message handlers registered")
        
        logger.info("All handlers registered successfully")
        
    except Exception as e:
        logger.error(f"Failed to register handlers: {e}")
        raise
