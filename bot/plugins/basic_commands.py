"""
Basic commands plugin for the Telegram bot.
Demonstrates how to create modular command plugins.
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.logger import setup_logger
from bot.utils.decorators import error_handler, track_usage, rate_limit

logger = setup_logger(__name__)

class BasicCommandsPlugin:
    """Plugin containing basic utility commands."""
    
    def __init__(self, client: Client):
        self.client = client
        self.name = "Basic Commands"
        self.version = "1.0.0"
        self.description = "Basic utility commands for the bot"
    
    def register(self):
        """Register all plugin commands."""
        self._register_echo_command()
        self._register_ping_command()
        self._register_time_command()
        self._register_count_command()
        logger.info(f"Plugin '{self.name}' registered successfully")
    
    def _register_echo_command(self):
        """Register echo command that repeats user input."""
        
        @self.client.on_message(filters.command("echo"))
        @error_handler
        @track_usage
        @rate_limit(max_requests=10, window=60)
        async def echo_command(client: Client, message: Message):
            """Echo the user's message."""
            # Get the text after the command
            if len(message.command) > 1:
                echo_text = " ".join(message.command[1:])
                response = f"🔄 **Echo:**\n{echo_text}"
            else:
                response = (
                    "🔄 **Echo Command**\n\n"
                    "Usage: `/echo <text>`\n"
                    "Example: `/echo Hello World!`\n\n"
                    "I'll repeat whatever you type after the command."
                )
            
            await message.reply_text(response)
    
    def _register_ping_command(self):
        """Register ping command to test bot responsiveness."""
        
        @self.client.on_message(filters.command("ping"))
        @error_handler
        @track_usage
        async def ping_command(client: Client, message: Message):
            """Respond with pong to test bot responsiveness."""
            import time
            
            start_time = time.time()
            
            # Send initial response
            sent_message = await message.reply_text("🏓 Pinging...")
            
            # Calculate response time
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            # Edit message with ping result
            await sent_message.edit_text(
                f"🏓 **Pong!**\n"
                f"Response time: {response_time:.2f}ms\n"
                f"Status: ✅ Online"
            )
    
    def _register_time_command(self):
        """Register time command to show current time."""
        
        @self.client.on_message(filters.command("time"))
        @error_handler
        @track_usage
        async def time_command(client: Client, message: Message):
            """Show current time and date."""
            from datetime import datetime
            import pytz
            
            # Get current UTC time
            utc_now = datetime.utcnow()
            
            # Format time string
            time_info = (
                f"🕐 **Current Time**\n\n"
                f"**UTC:** {utc_now.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"**Unix Timestamp:** {int(utc_now.timestamp())}\n"
                f"**ISO Format:** {utc_now.isoformat()}Z\n\n"
                f"📍 All times shown in UTC timezone"
            )
            
            await message.reply_text(time_info)
    
    def _register_count_command(self):
        """Register count command to count characters/words."""
        
        @self.client.on_message(filters.command("count"))
        @error_handler
        @track_usage
        async def count_command(client: Client, message: Message):
            """Count characters and words in the provided text."""
            
            if len(message.command) > 1:
                text_to_count = " ".join(message.command[1:])
                
                # Count statistics
                char_count = len(text_to_count)
                char_count_no_spaces = len(text_to_count.replace(" ", ""))
                word_count = len(text_to_count.split())
                line_count = len(text_to_count.split('\n'))
                
                response = (
                    f"🔢 **Text Statistics**\n\n"
                    f"**Characters:** {char_count}\n"
                    f"**Characters (no spaces):** {char_count_no_spaces}\n"
                    f"**Words:** {word_count}\n"
                    f"**Lines:** {line_count}\n\n"
                    f"**Text preview:**\n`{text_to_count[:100]}{'...' if len(text_to_count) > 100 else ''}`"
                )
            else:
                response = (
                    "🔢 **Count Command**\n\n"
                    "Usage: `/count <text>`\n"
                    "Example: `/count Hello world!`\n\n"
                    "I'll count characters, words, and lines in your text."
                )
            
            await message.reply_text(response)
