"""
Message handlers for the Telegram bot.
Handles text messages and provides automated responses.
"""

import re
import asyncio
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from bot.utils.logger import setup_logger
from bot.utils.decorators import error_handler, track_usage
from bot.config import config

logger = setup_logger(__name__)

def register_message_handlers(client: Client):
    """Register all message handlers."""
    
    @client.on_message(filters.text & ~filters.command([
        "start", "help", "info", "stats", "admin", "shutdown"
    ]))
    @error_handler
    @track_usage
    async def handle_text_messages(client: Client, message: Message):
        """Handle regular text messages with automated responses."""
        text = message.text.lower().strip()
        user = message.from_user
        
        # Check if this is a video URL - let the video downloader handle it
        supported_platforms = ["tiktok.com", "youtu.be", "youtube.com", "instagram.com"]
        if any(platform in text for platform in supported_platforms):
            return  # Let video downloader plugin handle this
        
        # Log the message
        logger.info(f"Text message from {user.id} (@{user.username}): {text[:50]}...")
        
        # Determine response based on message content
        response = await generate_response(text, message)
        
        if response:
            # Add typing simulation for more natural feel
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)  # Simulate typing delay
            
            await message.reply_text(response)
    
    @client.on_message(filters.photo)
    @error_handler
    @track_usage
    async def handle_photo_messages(client: Client, message: Message):
        """Handle photo messages."""
        user = message.from_user
        logger.info(f"Photo received from {user.id} (@{user.username})")
        
        responses = [
            "📸 Nice photo! I can see you shared an image.",
            "🖼️ Thanks for sharing the photo!",
            "📷 I received your image. Looks interesting!",
        ]
        
        import random
        response = random.choice(responses)
        await message.reply_text(response)
    
    @client.on_message(filters.document)
    @error_handler
    @track_usage
    async def handle_document_messages(client: Client, message: Message):
        """Handle document messages."""
        user = message.from_user
        document = message.document
        
        logger.info(f"Document received from {user.id}: {document.file_name}")
        
        response = (
            f"📄 Thanks for sharing the document!\n"
            f"**File:** {document.file_name}\n"
            f"**Size:** {document.file_size} bytes\n"
            f"**Type:** {document.mime_type or 'Unknown'}"
        )
        
        await message.reply_text(response)
    
    @client.on_message(filters.voice)
    @error_handler
    @track_usage
    async def handle_voice_messages(client: Client, message: Message):
        """Handle voice messages."""
        user = message.from_user
        voice = message.voice
        
        logger.info(f"Voice message received from {user.id}")
        
        response = (
            f"🎤 Thanks for the voice message!\n"
            f"**Duration:** {voice.duration} seconds\n"
            f"**Size:** {voice.file_size} bytes\n\n"
            f"I can't process voice messages yet, but I received it!"
        )
        
        await message.reply_text(response)
    
    @client.on_message(filters.sticker)
    @error_handler
    @track_usage
    async def handle_sticker_messages(client: Client, message: Message):
        """Handle sticker messages."""
        user = message.from_user
        logger.info(f"Sticker received from {user.id}")
        
        responses = [
            "😄 Cool sticker!",
            "🎭 Nice sticker choice!",
            "✨ Thanks for the sticker!",
            "😊 I like that sticker!",
        ]
        
        import random
        response = random.choice(responses)
        await message.reply_text(response)
    
    logger.info("Message handlers registered successfully")

async def generate_response(text: str, message: Message):
    """Generate automated response based on message content."""
    
    # Azerbaijani greeting patterns
    greeting_patterns = [
        r'\b(salam|salaam|salamlar)\b',
        r'\b(hello|hi|hey)\b',
        r'\b(sabahınız|günortanız|axşamınız)\s+(xeyir|xeyr)\b',
        r'\bnə\s+var\s+nə\s+yox\b'
    ]
    
    # Help/question patterns
    help_patterns = [
        r'\b(kömək|help|yardım)\b',
        r'\bnecə\s+(işləyir|istifadə)\b',
        r'\bnə\s+edə\s+bilir\b',
        r'\bnə\s+üçün\b'
    ]
    
    # Gratitude patterns in Azerbaijani
    thanks_patterns = [
        r'\b(təşəkkür|sağol|çox\s+sağol)\b',
        r'\b(thank|thanks|thx)\b',
        r'\bminnətdaram\b'
    ]
    
    # Check for greetings (respond only to greetings)
    for pattern in greeting_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return f"Salam {message.from_user.first_name}! Video endirmək üçün sadəcə link göndərin."
    
    # Check for help requests
    for pattern in help_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return (
                "Video endirmək üçün:\n"
                "• TikTok linki göndərin\n"
                "• Instagram linki göndərin\n"
                "• YouTube linki göndərin\n\n"
                "Komandlar üçün /help yazın."
            )
    
    # Check for thanks
    for pattern in thanks_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "Rica edirəm! Başqa bir şey lazımdırsa söyləyin."
    
    # Return None for other messages (no response)
    return None
