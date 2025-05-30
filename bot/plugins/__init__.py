"""
Plugins package for the Telegram bot.
Contains modular plugin implementations for easy extension.
"""

from .basic_commands import BasicCommandsPlugin
from .video_downloader import VideoDownloaderPlugin

# Available plugins
AVAILABLE_PLUGINS = [
    BasicCommandsPlugin,
    VideoDownloaderPlugin,
]

def load_all_plugins(client):
    """Load all available plugins."""
    from bot.utils.logger import setup_logger
    
    logger = setup_logger(__name__)
    
    for plugin_class in AVAILABLE_PLUGINS:
        try:
            plugin = plugin_class(client)
            plugin.register()
            logger.info(f"Plugin '{plugin_class.__name__}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load plugin '{plugin_class.__name__}': {e}")
