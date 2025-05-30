#!/usr/bin/env python3

import asyncio
import signal
import sys
from bot.client import TelegramBot
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)
bot_instance = None

def signal_handler(signum, frame):
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    if bot_instance:
        asyncio.create_task(bot_instance.stop())
    sys.exit(0)

async def main():
    """Main function to initialize and run the bot."""
    global bot_instance
    
    try:
        # Initialize the bot
        bot_instance = TelegramBot()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Starting Telegram bot...")
        
        # Start the bot
        await bot_instance.start()
        
        logger.info("Bot started successfully!")
        logger.info("Press Ctrl+C to stop the bot")
        
        # Keep the bot running
        await bot_instance.idle()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)
    finally:
        if bot_instance:
            await bot_instance.stop()
        logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
