"""
Azerbaijani localization for the Telegram bot.
"""

# Command messages
COMMANDS = {
    'start': {
        'text': """👋 Salam! Mən video endirmə botuyam.

📱 Dəstəklədiyim platformalar:
• Instagram (Reels, Posts, Stories)
• TikTok videoları
• YouTube videoları (məhdud)

📋 Əsas əmrlər:
/help - Kömək məlumatları
/info - Bot haqqında məlumat
/stats - Statistikalar
/language - Dil dəyişdir

🔗 Video linkini göndərin və mən onu sizə yükləyəcəyəm!"""
    },
    'help': {
        'text': """❓ Kömək məlumatları

🎯 Bot necə işləyir:
1. Video linki göndərin
2. Bot videoları emal edəcək
3. Video sizə göndəriləcək

📱 Dəstəklənən platformalar:
• Instagram - Tam dəstək
• TikTok - Tam dəstək  
• YouTube - Məhdud dəstək

💡 Məsləhətlər:
• Qısa linklər (youtu.be) əvəzinə tam linklərdən istifadə edin
• Şəxsi hesabların videolarını yükləmək mümkün olmaya bilər
• Böyük faylların yüklənməsi daha çox vaxt ala bilər

❌ Problemlər:
Əgər problem yaşayırsınızsa, başqa link cəhd edin və ya admin ilə əlaqə saxlayın."""
    },
    'info': {
        'text': """ℹ️ Bot haqqında

🤖 Ad: Silgi Video Endirmə Botu
🔧 Versiya: 2.0.0
⚡ Texnologiya: Pyrogram + yt-dlp

🌟 Xüsusiyyətlər:
• Sürətli video endirmə
• Çoxlu platform dəstəyi
• Yüklənmə irəliləyiş göstəricisi
• Avtomatik fayl təmizləmə

📊 Performans:
• Instagram: Əla
• TikTok: Əla
• YouTube: Məhdud

🛡️ Təhlükəsizlik:
Bütün fayllar müvəqqəti saxlanılır və avtomatik silinir."""
    },
    'help': {
        'text': """🤖 Silgi Video Yükləmə Botu

📥 Dəstəklənən platformalar:
• Instagram (Reels, videolar)
• TikTok (videolar) 
• YouTube (məhdud)

🔧 Əmrlər:
/start - Botu başlat və dil seç
/help - Bu yardım mətni
/info - Bot haqqında məlumat
/stats - İstifadə statistikaları
/language - Dili dəyişdir

📝 İstifadə:
Video linkini göndərin və bot avtomatik yükləyəcək.

⚠️ Qeyd: YouTube platformasında məhdudiyyətlər var."""
    },
    'info': {
        'text': """ℹ️ Bot haqqında

🤖 Ad: Silgi Video Endirmə Botu
🔧 Versiya: 2.0.0
⚡ Texnologiya: Pyrogram + yt-dlp

🌟 Xüsusiyyətlər:
• Sürətli video endirmə
• Çoxlu platform dəstəyi
• Yüklənmə irəliləyiş göstəricisi
• Avtomatik fayl təmizləmə

📊 Performans:
• Instagram: Əla
• TikTok: Əla
• YouTube: Məhdud

🛡️ Təhlükəsizlik:
Bütün fayllar müvəqqəti saxlanılır və avtomatik silinir."""
    },
    'stats': {
        'text': """📊 Statistikalar

👤 İstifadəçi: {username}
🆔 ID: {user_id}
📅 İlk istifadə: {first_use}
📈 Ümumi sorğular: {total_requests}
⬇️ Uğurlu yüklənmələr: {successful_downloads}

🏆 Platform statistikaları:
• Instagram: {instagram_count}
• TikTok: {tiktok_count}  
• YouTube: {youtube_count}

⚡ Son fəaliyyət: {last_activity}"""
    }
}

# Status messages
STATUS = {
    'processing': '🔄 Video linki emal edilir...',
    'downloading': '⬇️ Video yüklənir ({platform})...',
    'uploading': '📤 Video göndərilir...',
    'success': '✅ Video uğurla göndərildi!',
    'error': '❌ Xəta baş verdi: {error}',
    'not_supported': '❌ Bu link dəstəklənmir. Instagram, TikTok və ya YouTube linkləri göndərin.',
    'invalid_link': '❌ Yanlış link formatı. Düzgün video linki göndərin.',
    'file_too_large': '❌ Fayl çox böyükdür. Daha kiçik video cəhd edin.',
    'download_failed': '❌ Video yüklənə bilmədi. Linki yoxlayın və yenidən cəhd edin.'
}

# YouTube specific messages
YOUTUBE = {
    'restrictions': """⚠️ YouTube sərt yüklənmə məhdudiyyətləri qoyub.
Zəhmət olmasa cəhd edin:
• Instagram və ya TikTok linkləri
• Fərqli YouTube videosu
• Daha qısa və ya köhnə YouTube videoları""",
    'signin_required': '🔐 YouTube giriş tələb edir. Instagram və ya TikTok istifadə edin.',
    'format_unavailable': '📺 Video formatı mövcud deyil. Başqa video cəhd edin.'
}

# Progress messages
PROGRESS = {
    'downloading': '⬇️ Yüklənir: {percentage}% ({size})',
    'processing': '⚙️ Emal edilir...',
    'uploading': '📤 Telegram-a göndərilir: {percentage}%',
    'finalizing': '🎬 Tamamlanır...'
}

# Platform names
PLATFORMS = {
    'instagram': 'Instagram',
    'youtube': 'YouTube', 
    'tiktok': 'TikTok'
}

# Language selection
LANGUAGE = {
    'select': 'Zəhmət olmasa dilinizi seçin:',
    'changed': 'Dil Azərbaycan dilinə dəyişdirildi ✅',
    'flag': '🇦🇿'
}

# Error messages
ERRORS = {
    'network': '🌐 Şəbəkə xətası. Yenidən cəhd edin.',
    'timeout': '⏱️ Vaxt doldu. Daha kiçik fayl cəhd edin.',
    'forbidden': '🚫 Giriş qadağandır. Başqa video cəhd edin.',
    'not_found': '🔍 Video tapılmadı. Linki yoxlayın.',
    'server_error': '🔧 Server xətası. Bir az sonra cəhd edin.',
    'rate_limit': '⚡ Çox sürətli! Bir az gözləyin və yenidən cəhd edin.',
    'file_corrupt': '💾 Fayl zədələnib. Yenidən yükləyin.',
    'unsupported_format': '📄 Dəstəklənməyən format. MP4 video cəhd edin.'
}

# Promotional messages
PROMOTIONAL = {
    'groups': '🎭 Daha çox botlar və xidmətlər üçün qruplarımıza qoşulun:'
}

# File size formatting
def format_size(bytes_size):
    """Format file size in Azerbaijani"""
    if bytes_size is None:
        return "bilinmir"
    
    for unit in ['bayt', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def create_progress_bar(percentage, length=10):
    """Create visual progress bar"""
    filled = int(length * percentage / 100)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {percentage}%"