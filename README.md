<div align="center">

# 🎬 Multilingual Telegram Video Downloader Bot

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=30&duration=3000&pause=1000&color=36BCF7&center=true&vCenter=true&multiline=true&width=800&height=100&lines=Download+Videos+from+TikTok%2C+Instagram%2C+YouTube;Support+for+4+Languages;Real-time+Progress+Tracking" alt="Typing SVG" />

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Silgimusicbot/multilingual-telegram-video-bot?style=for-the-badge)](https://github.com/Silgimusicbot/multilingual-telegram-video-bot/stargazers)

*A sophisticated Telegram bot that downloads videos from multiple platforms with full multilingual support*

</div>

---

## ✨ Features

<div align="center">

| 🎯 **Platform Support** | 🌍 **Languages** | 🔧 **Core Features** |
|:----------------------:|:----------------:|:--------------------:|
| TikTok | 🇦🇿 Azerbaijani | Video Title Extraction |
| Instagram | 🇺🇸 English | Progress Tracking |
| YouTube | 🇹🇷 Turkish | User Preferences |
| | 🇷🇺 Russian | Admin Commands |

</div>

### 🚀 **Core Capabilities**
- **📱 Multi-Platform Downloads**: Seamless video downloading from TikTok, Instagram, and YouTube
- **🌐 4-Language Support**: Complete localization for Azerbaijani, English, Turkish, and Russian
- **🎬 Smart Title Extraction**: Automatically extracts and displays video titles and metadata
- **📊 Real-time Progress**: Visual progress bars with file size information
- **💾 User Preferences**: Persistent language settings for each user
- **🔗 Community Integration**: Built-in promotional messages for Telegram groups
- **🔧 Plugin Architecture**: Modular design for easy feature expansion
- **🛡️ Advanced Error Handling**: Comprehensive logging and error management
- **👑 Admin Controls**: Special administrative commands and analytics

---

## 🎮 Quick Start

<details>
<summary>🔧 <b>Prerequisites</b></summary>

- Python 3.8 or higher
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Telegram API credentials from [my.telegram.org](https://my.telegram.org)

</details>

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Silgimusicbot/multilingual-telegram-video-bot.git
cd multilingual-telegram-video-bot

# Install dependencies
pip install pyrogram python-dotenv pytz yt-dlp instaloader requests

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python main.py
```

### ⚙️ Configuration

Create a `.env` file with your credentials:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
ADMIN_IDS=your_user_id_here
```

---

## 🎯 Commands & Usage

<div align="center">

### 📋 **Available Commands**

| Command | Description | Access Level |
|---------|-------------|--------------|
| `/start` | Initialize bot and select language | 👤 All Users |
| `/language` | Change language preference | 👤 All Users |
| `/help` | Display help information | 👤 All Users |
| `/info` | Show bot information | 👤 All Users |
| `/stats` | View usage statistics | 👤 All Users |
| `/admin` | Access admin panel | 👑 Admin Only |

</div>

### 🎬 **Video Download Process**

1. **Send a video URL** from TikTok, Instagram, or YouTube
2. **Watch real-time progress** with visual indicators
3. **Receive the video** with title and metadata in your language
4. **Enjoy seamless downloads** with automatic error handling

---

## 🌍 Language Support

<div align="center">

<table>
<tr>
<td align="center">🇦🇿<br><b>Azerbaijani</b><br><code>az</code></td>
<td align="center">🇺🇸<br><b>English</b><br><code>en</code></td>
<td align="center">🇹🇷<br><b>Turkish</b><br><code>tr</code></td>
<td align="center">🇷🇺<br><b>Russian</b><br><code>ru</code></td>
</tr>
</table>

</div>

---

## 📱 Supported Platforms

<div align="center">

### 🎵 **TikTok**
- Full video downloads with metadata
- Enhanced title extraction
- Support for all video formats

### 📸 **Instagram**
- Reels and video posts
- Story downloads
- High-quality video extraction

### 🎥 **YouTube**
- Video downloads with metadata
- Multiple quality options
- Advanced bypass techniques

</div>

---

## 🏗️ Project Architecture

```
📁 multilingual-telegram-video-bot/
├── 🤖 bot/
│   ├── 📡 handlers/          # Message and command processors
│   ├── 🌍 localization/      # 4-language translation files
│   ├── 🔌 plugins/           # Modular feature implementations
│   ├── 🛠️ utils/             # Core utilities and helpers
│   ├── 🚀 client.py          # Main bot client
│   └── ⚙️ config.py          # Configuration management
├── 🎯 main.py                # Application entry point
├── 📚 README.md              # Documentation
├── 🔒 .env.example           # Environment template
└── 📝 pyproject.toml         # Project dependencies
```

---

## 🔌 Plugin System

<div align="center">

| Plugin | Features | Status |
|--------|----------|--------|
| **BasicCommandsPlugin** | Essential utility commands | ✅ Active |
| **VideoDownloaderPlugin** | Multi-platform video downloads | ✅ Active |

</div>

---

## 📊 Key Features Breakdown

### 🎬 **Video Processing**
- Automatic platform detection from URLs
- Real-time progress tracking with visual indicators
- Intelligent file size formatting in user's language
- Comprehensive error handling for failed downloads
- Multilingual video captions and metadata

### 🌐 **Internationalization**
- Dynamic language switching mid-conversation
- Persistent user language preferences
- Culturally appropriate formatting (dates, sizes)
- Complete UI localization for all features

### 👑 **Administration**
- Comprehensive user analytics and statistics
- Admin-only command access control
- Bot usage monitoring and reporting
- Graceful shutdown and restart capabilities

---

## 🤝 Community & Support

<div align="center">

### 📱 **Official Telegram Channels**

[![Bot Updates](https://img.shields.io/badge/Bot%20Updates-@silgiuserbots-blue?style=for-the-badge&logo=telegram)](https://t.me/silgiuserbots)
[![Community](https://img.shields.io/badge/Community-@silgiub-green?style=for-the-badge&logo=telegram)](https://t.me/silgiub)
[![Support Chat](https://img.shields.io/badge/Support%20Chat-@silgiuserbotchat-orange?style=for-the-badge&logo=telegram)](https://t.me/silgiuserbotchat)

</div>

---

## 🤝 Contributing

We welcome contributions! Please feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. 💻 Make your improvements
4. ✅ Add tests if applicable
5. 📤 Submit a pull request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🎯 **Author**

**Created with ❤️ by [SILGI](https://t.me/silgiteam)**

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=20&duration=2000&pause=1000&color=36BCF7&center=true&vCenter=true&width=600&lines=Building+the+Future+of+Telegram+Bots;Multilingual+%7C+Fast+%7C+Reliable" alt="Footer Typing SVG" />

---

⭐ **If you found this project helpful, please give it a star!** ⭐

</div>