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

async def generate_response(text: str, message: Message) -> str:
    """Generate automated response based on message content."""
    
    # Greeting patterns
    greeting_patterns = [
        r'\b(hi|hello|hey|greetings?)\b',
        r'\bgood\s+(morning|afternoon|evening|day)\b',
        r'\bwhat\'?s\s+up\b'
    ]
    
    # Question patterns
    question_patterns = [
        r'\bwhat\b.*\?',
        r'\bhow\b.*\?',
        r'\bwhy\b.*\?',
        r'\bwhen\b.*\?',
        r'\bwhere\b.*\?',
        r'\bwho\b.*\?'
    ]
    
    # Gratitude patterns
    thanks_patterns = [
        r'\b(thank|thanks|thx)\b',
        r'\bappreciate\b',
        r'\bgrateful\b'
    ]
    
    # Bot-related patterns
    bot_patterns = [
        r'\b(bot|robot|ai|artificial)\b',
        r'\bare\s+you\s+(real|human|alive)\b',
        r'\bwhat\s+are\s+you\b'
    ]
    
    # Check for greetings
    for pattern in greeting_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return f"👋 Hello {message.from_user.first_name}! How can I help you today?"
    
    # Check for questions
    for pattern in question_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return (
                "🤔 That's an interesting question! I'm a simple bot built with Pyrogram. "
                "For more complex queries, you might want to contact my developer or use /help to see what I can do."
            )
    
    # Check for thanks
    for pattern in thanks_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return "😊 You're welcome! I'm happy to help. Is there anything else you need?"
    
    # Check for bot-related queries
    for pattern in bot_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return (
                "🤖 Yes, I'm a Telegram bot built with Pyrogram! "
                "I can respond to commands, handle messages, and assist with various tasks. "
                "Use /info to learn more about my capabilities!"
            )
    
    # Check message length for different responses
    if len(text) > 100:
        return (
            "📝 That's quite a long message! I read it all. "
            "While I can't provide complex analysis yet, I appreciate you sharing your thoughts with me."
        )
    
    # Check for specific keywords
    if any(word in text for word in ['help', 'support', 'assist']):
        return "🆘 I'm here to help! Use /help to see available commands or just tell me what you need."
    
    if any(word in text for word in ['bye', 'goodbye', 'see you', 'farewell']):
        return f"👋 Goodbye {message.from_user.first_name}! Feel free to message me anytime!"
    
    if any(word in text for word in ['weather', 'temperature', 'forecast']):
        return "🌤️ I don't have weather information yet, but that's a great feature idea for future updates!"
    
    # Default responses for general messages
    default_responses = [
        "💭 Interesting! Tell me more about that.",
        "🤖 I received your message! Thanks for chatting with me.",
        "✨ That's nice! I'm learning to have better conversations.",
        "📨 Message received! I'm a simple bot, but I'm here to chat.",
        "🎯 I understand you're trying to communicate with me. How can I help?",
        "💬 Thanks for the message! Feel free to ask me anything or use /help for available commands.",
    ]
    
    import random
    return random.choice(default_responses)
