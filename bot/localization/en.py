"""
English localization for the Telegram bot.
"""

# Command messages
COMMANDS = {
    'start': {
        'text': """👋 Hello! I'm a video downloader bot.

📱 Supported platforms:
• Instagram (Reels, Posts, Stories)
• TikTok videos
• YouTube videos (limited)

📋 Main commands:
/help - Help information
/info - Bot information
/stats - Statistics
/language - Change language

🔗 Send me a video link and I'll download it for you!"""
    },
    'help': {
        'text': """❓ Help Information

🎯 How the bot works:
1. Send a video link
2. Bot will process the video
3. Video will be sent to you

📱 Supported platforms:
• Instagram - Full support
• TikTok - Full support
• YouTube - Limited support

💡 Tips:
• Use full links instead of short links (youtu.be)
• Private account videos may not be downloadable
• Large files may take longer to upload

❌ Problems:
If you experience issues, try another link or contact admin."""
    },
    'info': {
        'text': """ℹ️ About Bot

🤖 Name: Silgi Video Downloader Bot
🔧 Version: 2.0.0
⚡ Technology: Pyrogram + yt-dlp

🌟 Features:
• Fast video downloading
• Multiple platform support
• Download progress indicator
• Automatic file cleanup

📊 Performance:
• Instagram: Excellent
• TikTok: Excellent
• YouTube: Limited

🛡️ Security:
All files are temporarily stored and automatically deleted."""
    },
    'help': {
        'text': """🤖 Silgi Video Download Bot

📥 Supported platforms:
• Instagram (Reels, videos)
• TikTok (videos) 
• YouTube (limited)

🔧 Commands:
/start - Start bot and select language
/help - This help message
/info - Bot information
/stats - Usage statistics
/language - Change language

📝 Usage:
Send a video link and the bot will download it automatically.

⚠️ Note: YouTube has restrictions."""
    },
    'info': {
        'text': """ℹ️ About Bot

🤖 Name: Silgi Video Download Bot
🔧 Version: 2.0.0
⚡ Technology: Pyrogram + yt-dlp

🌟 Features:
• Fast video downloading
• Multiple platform support
• Download progress indicators
• Automatic file cleanup

📊 Performance:
• Instagram: Excellent
• TikTok: Excellent
• YouTube: Limited

🛡️ Security:
All files are temporarily stored and automatically deleted."""
    },
    'stats': {
        'text': """📊 Statistics

👤 User: {username}
🆔 ID: {user_id}
📅 First use: {first_use}
📈 Total requests: {total_requests}
⬇️ Successful downloads: {successful_downloads}

🏆 Platform statistics:
• Instagram: {instagram_count}
• TikTok: {tiktok_count}
• YouTube: {youtube_count}

⚡ Last activity: {last_activity}"""
    }
}

# Status messages
STATUS = {
    'processing': '🔄 Processing video link...',
    'downloading': '⬇️ Downloading video ({platform})...',
    'uploading': '📤 Uploading video...',
    'success': '✅ Video sent successfully!',
    'error': '❌ Error occurred: {error}',
    'not_supported': '❌ This link is not supported. Send Instagram, TikTok or YouTube links.',
    'invalid_link': '❌ Invalid link format. Send a proper video link.',
    'file_too_large': '❌ File is too large. Try a smaller video.',
    'download_failed': '❌ Could not download video. Check the link and try again.'
}

# YouTube specific messages
YOUTUBE = {
    'restrictions': """⚠️ YouTube has strict download restrictions.
Please try:
• Instagram or TikTok links
• Different YouTube video
• Shorter or older YouTube videos""",
    'signin_required': '🔐 YouTube requires sign in. Use Instagram or TikTok.',
    'format_unavailable': '📺 Video format unavailable. Try another video.'
}

# Progress messages
PROGRESS = {
    'downloading': '⬇️ Downloading: {percentage}% ({size})',
    'processing': '⚙️ Processing...',
    'uploading': '📤 Uploading to Telegram: {percentage}%',
    'finalizing': '🎬 Finalizing...'
}

# Platform names
PLATFORMS = {
    'instagram': 'Instagram',
    'youtube': 'YouTube',
    'tiktok': 'TikTok'
}

# Language selection
LANGUAGE = {
    'select': 'Please select your language:',
    'changed': 'Language changed to English ✅',
    'flag': '🇺🇸'
}

# File size formatting
def format_size(bytes_size):
    """Format file size in English"""
    if bytes_size is None:
        return "unknown"
    
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def create_progress_bar(percentage, length=10):
    """Create visual progress bar"""
    filled = int(length * percentage / 100)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {percentage}%"

# Promotional messages
PROMOTIONAL = {
    'groups': '🎭 Join our groups for more bots and services:'
}