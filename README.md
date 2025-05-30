# Multilingual Telegram Video Downloader Bot

A sophisticated Telegram bot that downloads videos from TikTok, Instagram, and YouTube with full multilingual support and video title extraction.

## 🌟 Features

- **Multi-Platform Video Downloads**: Supports TikTok, Instagram, and YouTube
- **4-Language Support**: Azerbaijani, English, Turkish, and Russian
- **Video Title Extraction**: Automatically extracts and displays video titles
- **Real-time Progress Tracking**: Shows download and upload progress with progress bars
- **User Language Preferences**: Remembers each user's preferred language
- **Promotional Integration**: Includes promotional messages for Telegram groups
- **Plugin Architecture**: Modular design for easy extension
- **Advanced Error Handling**: Comprehensive logging and error management
- **Admin Commands**: Special commands for bot administrators

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Telegram Bot Token
- Telegram API credentials

### Installation

1. Install dependencies:
```bash
pip install pyrogram python-dotenv pytz yt-dlp instaloader requests
```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your Telegram credentials

3. Run the bot:
```bash
python main.py
```

## 🔧 Configuration

Create a `.env` file with the following variables:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
ADMIN_IDS=your_user_id_here
```

## 🎯 Commands

- `/start` - Start the bot and select language
- `/language` - Change language preference
- `/help` - Show help information
- `/info` - Display bot information
- `/stats` - Show user statistics
- `/admin` - Admin panel (admin only)

## 🌐 Supported Languages

- 🇦🇿 Azerbaijani (az)
- 🇺🇸 English (en)
- 🇹🇷 Turkish (tr)
- 🇷🇺 Russian (ru)

## 📱 Supported Platforms

- **TikTok**: Full video downloads with title extraction
- **Instagram**: Reels and video posts
- **YouTube**: Video downloads with metadata

## 🏗️ Project Structure

```
bot/
├── handlers/          # Message and command handlers
├── localization/      # Language files for 4 languages
├── plugins/           # Video downloader and utility plugins
├── utils/            # Language manager and utilities
├── client.py         # Main bot client
└── config.py         # Configuration management

main.py               # Entry point
```

## 🔌 Plugin System

The bot uses a modular plugin system:

- **BasicCommandsPlugin**: Essential utility commands
- **VideoDownloaderPlugin**: Video downloading functionality

## 📊 Video Download Features

- Automatic platform detection from URLs
- Progress tracking with visual progress bars
- File size formatting in user's language
- Video title extraction and display
- Error handling for failed downloads
- Multilingual captions for downloaded videos

## 🤝 Community Links

- [@silgiuserbots](https://t.me/silgiuserbots) - Bot Updates
- [@silgiub](https://t.me/silgiub) - Community
- [@silgiuserbotchat](https://t.me/silgiuserbotchat) - Support Chat

## 📄 License

MIT License