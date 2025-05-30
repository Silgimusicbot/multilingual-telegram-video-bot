"""
Logging utilities for the Telegram bot.
Provides structured logging with proper formatting and file output.
"""

import logging
import sys
from typing import Optional
from datetime import datetime
from bot.config import config

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with proper formatting and handlers.
    
    Args:
        name: Logger name (usually __name__)
        level: Log level override
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Set log level
    log_level = level or config.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if configured)
    if config.LOG_FILE:
        try:
            file_handler = logging.FileHandler(config.LOG_FILE, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not set up file logging: {e}")
    
    return logger

class BotLogger:
    """Enhanced logger class with bot-specific methods."""
    
    def __init__(self, name: str):
        self.logger = setup_logger(name)
    
    def command_used(self, user_id: int, username: str, command: str, chat_type: str = "private"):
        """Log command usage."""
        self.logger.info(
            f"Command '{command}' used by {user_id} (@{username}) in {chat_type} chat"
        )
    
    def message_received(self, user_id: int, username: str, message_type: str, chat_id: int):
        """Log message reception."""
        self.logger.info(
            f"{message_type.title()} message from {user_id} (@{username}) in chat {chat_id}"
        )
    
    def error_occurred(self, error: Exception, context: str = ""):
        """Log errors with context."""
        self.logger.error(f"Error in {context}: {type(error).__name__}: {error}")
    
    def user_joined(self, user_id: int, username: str, chat_id: int):
        """Log user joining."""
        self.logger.info(f"User {user_id} (@{username}) joined chat {chat_id}")
    
    def user_left(self, user_id: int, username: str, chat_id: int):
        """Log user leaving."""
        self.logger.info(f"User {user_id} (@{username}) left chat {chat_id}")
    
    def bot_started(self, bot_username: str, bot_id: int):
        """Log bot startup."""
        self.logger.info(f"Bot @{bot_username} (ID: {bot_id}) started successfully")
    
    def bot_stopped(self):
        """Log bot shutdown."""
        self.logger.info("Bot stopped gracefully")

# Create a global bot logger instance
bot_logger = BotLogger("telegram_bot")
