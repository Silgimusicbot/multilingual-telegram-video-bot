"""
Decorators for the Telegram bot.
Provides error handling, usage tracking, and other utilities.
"""

import asyncio
import functools
import time
from typing import Dict, List
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

# Rate limiting storage
user_rate_limits: Dict[int, List[float]] = {}

def error_handler(func):
    """Decorator to handle errors in handler functions."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Extract message from args to get user info
            message = None
            for arg in args:
                if isinstance(arg, Message):
                    message = arg
                    break
            
            error_context = f"handler '{func.__name__}'"
            if message:
                username = message.from_user.username or "No username"
                user_info = f"user {message.from_user.id} (@{username})"
                error_context += f" for {user_info}"
            
            logger.error(f"Error in {error_context}: {type(e).__name__}: {e}")
            
            # Send user-friendly error message if possible
            if message:
                try:
                    await message.reply_text(
                        "⚠️ Sorry, something went wrong while processing your request. "
                        "The error has been logged and will be investigated."
                    )
                except Exception as reply_error:
                    logger.error(f"Failed to send error message: {reply_error}")
            
            # Re-raise critical errors
            if isinstance(e, (KeyboardInterrupt, SystemExit)):
                raise
    
    return wrapper

def track_usage(func):
    """Decorator to track command and message usage."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract message from args
        message = None
        for arg in args:
            if isinstance(arg, Message):
                message = arg
                break
        
        if message:
            user = message.from_user
            chat_type = str(message.chat.type).split('.')[-1].lower()
            
            # Determine the type of interaction
            if message.text and message.text.startswith('/'):
                interaction_type = f"command_{message.text.split()[0][1:]}"
            else:
                interaction_type = "message"
            
            username = user.username or "No username"
            logger.info(
                f"Usage tracking: {interaction_type} by {user.id} "
                f"(@{username}) in {chat_type} chat"
            )
        
        return await func(*args, **kwargs)
    
    return wrapper

def rate_limit(max_requests: int = 5, window: int = 60):
    """Decorator to implement rate limiting per user."""
    
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract message from args
            message = None
            for arg in args:
                if isinstance(arg, Message):
                    message = arg
                    break
            
            if not message:
                return await func(*args, **kwargs)
            
            user_id = message.from_user.id
            current_time = time.time()
            
            # Initialize user rate limit tracking
            if user_id not in user_rate_limits:
                user_rate_limits[user_id] = []
            
            # Clean old requests outside the window
            user_requests = user_rate_limits[user_id]
            user_requests[:] = [req_time for req_time in user_requests 
                              if current_time - req_time < window]
            
            # Check if user exceeded rate limit
            if len(user_requests) >= max_requests:
                username = message.from_user.username or "No username"
                logger.warning(
                    f"Rate limit exceeded for user {user_id} "
                    f"(@{username})"
                )
                
                await message.reply_text(
                    f"⚡ Slow down! You've sent too many requests. "
                    f"Please wait a moment before trying again."
                )
                return
            
            # Add current request to tracking
            user_requests.append(current_time)
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def admin_only(func):
    """Decorator to restrict access to admin users only."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        from bot.config import config
        
        # Extract message from args
        message = None
        for arg in args:
            if isinstance(arg, Message):
                message = arg
                break
        
        if not message:
            return await func(*args, **kwargs)
        
        user_id = message.from_user.id
        
        if user_id not in config.ADMIN_IDS:
            username = message.from_user.username or "No username"
            logger.warning(
                f"Unauthorized admin access attempt by {user_id} "
                f"(@{username})"
            )
            
            await message.reply_text(
                "🚫 Access denied. This command is restricted to administrators only."
            )
            return
        
        logger.info(f"Admin command executed by {user_id}")
        return await func(*args, **kwargs)
    
    return wrapper

def typing_action(func):
    """Decorator to show typing action while processing."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Extract client and message from args
        client = args[0] if args else None
        message = None
        
        for arg in args:
            if isinstance(arg, Message):
                message = arg
                break
        
        if client and message:
            # Start typing action
            typing_task = asyncio.create_task(
                client.send_chat_action(message.chat.id, ChatAction.TYPING)
            )
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                # Cancel typing action
                typing_task.cancel()
                try:
                    await typing_task
                except asyncio.CancelledError:
                    pass
        else:
            return await func(*args, **kwargs)
    
    return wrapper

def log_execution_time(func):
    """Decorator to log function execution time."""
    
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.debug(f"Function '{func.__name__}' executed in {execution_time:.3f}s")
            return result
        
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"Function '{func.__name__}' failed after {execution_time:.3f}s: {e}"
            )
            raise
    
    return wrapper
