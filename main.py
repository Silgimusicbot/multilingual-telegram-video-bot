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