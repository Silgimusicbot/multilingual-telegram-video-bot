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
        text = message.text.lower().strip()
        user = message.from_user
        
        supported_platforms = ["tiktok.com", "youtu.be", "youtube.com", "instagram.com"]
        if any(platform in text for platform in supported_platforms):
            return
        
        logger.info(f"Text message from {user.id} (@{user.username}): {text[:50]}...")
        
        response = await generate_response(text, message)
        
        if response:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            await asyncio.sleep(1)
            
            await message.reply_text(response)
    
    @client.on_message(filters.photo)
    @error_handler
    @track_usage
    async def handle_photo_messages(client: Client, message: Message):
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