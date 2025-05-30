"""
Turkish localization for the Telegram bot.
"""

# Command messages
COMMANDS = {
    'start': {
        'text': """👋 Merhaba! Ben bir video indirme botuyum.

📱 Desteklenen platformlar:
• Instagram (Reels, Posts, Stories)
• TikTok videoları
• YouTube videoları (sınırlı)

📋 Ana komutlar:
/help - Yardım bilgileri
/info - Bot hakkında bilgi
/stats - İstatistikler
/language - Dil değiştir

🔗 Bana bir video linki gönderin, sizin için indireceğim!"""
    },
    'help': {
        'text': """❓ Yardım Bilgileri

🎯 Bot nasıl çalışır:
1. Video linki gönderin
2. Bot videoyu işleyecek
3. Video size gönderilecek

📱 Desteklenen platformlar:
• Instagram - Tam destek
• TikTok - Tam destek
• YouTube - Sınırlı destek

💡 İpuçları:
• Kısa linkler (youtu.be) yerine tam linkler kullanın
• Özel hesap videoları indirilemeyebilir
• Büyük dosyalar daha uzun sürebilir

❌ Sorunlar:
Sorun yaşarsanız, başka bir link deneyin veya admin ile iletişime geçin."""
    },
    'info': {
        'text': """ℹ️ Bot Hakkında

🤖 Ad: Silgi Video İndirme Botu
🔧 Sürüm: 2.0.0
⚡ Teknoloji: Pyrogram + yt-dlp

🌟 Özellikler:
• Hızlı video indirme
• Çoklu platform desteği
• İndirme ilerleme göstergesi
• Otomatik dosya temizleme

📊 Performans:
• Instagram: Mükemmel
• TikTok: Mükemmel
• YouTube: Sınırlı

🛡️ Güvenlik:
Tüm dosyalar geçici olarak saklanır ve otomatik silinir."""
    },
    'help': {
        'text': """🤖 Silgi Video İndirme Botu

📥 Desteklenen platformlar:
• Instagram (Reels, videolar)
• TikTok (videolar) 
• YouTube (sınırlı)

🔧 Komutlar:
/start - Botu başlat ve dil seç
/help - Bu yardım mesajı
/info - Bot bilgileri
/stats - Kullanım istatistikleri
/language - Dil değiştir

📝 Kullanım:
Video linkini gönderin, bot otomatik olarak indirecek.

⚠️ Not: YouTube'da kısıtlamalar var."""
    },
    'info': {
        'text': """ℹ️ Bot Hakkında

🤖 Ad: Silgi Video İndirme Botu
🔧 Sürüm: 2.0.0
⚡ Teknoloji: Pyrogram + yt-dlp

🌟 Özellikler:
• Hızlı video indirme
• Çoklu platform desteği
• İndirme ilerleme göstergeleri
• Otomatik dosya temizleme

📊 Performans:
• Instagram: Mükemmel
• TikTok: Mükemmel
• YouTube: Sınırlı

🛡️ Güvenlik:
Tüm dosyalar geçici olarak saklanır ve otomatik silinir."""
    },
    'stats': {
        'text': """📊 İstatistikler

👤 Kullanıcı: {username}
🆔 ID: {user_id}
📅 İlk kullanım: {first_use}
📈 Toplam istekler: {total_requests}
⬇️ Başarılı indirmeler: {successful_downloads}

🏆 Platform istatistikleri:
• Instagram: {instagram_count}
• TikTok: {tiktok_count}
• YouTube: {youtube_count}

⚡ Son aktivite: {last_activity}"""
    }
}

# Status messages
STATUS = {
    'processing': '🔄 Video linki işleniyor...',
    'downloading': '⬇️ Video indiriliyor ({platform})...',
    'uploading': '📤 Video gönderiliyor...',
    'success': '✅ Video başarıyla gönderildi!',
    'error': '❌ Hata oluştu: {error}',
    'not_supported': '❌ Bu link desteklenmiyor. Instagram, TikTok veya YouTube linki gönderin.',
    'invalid_link': '❌ Geçersiz link formatı. Düzgün bir video linki gönderin.',
    'file_too_large': '❌ Dosya çok büyük. Daha küçük bir video deneyin.',
    'download_failed': '❌ Video indirilemedi. Linki kontrol edin ve tekrar deneyin.'
}

# YouTube specific messages
YOUTUBE = {
    'restrictions': """⚠️ YouTube sıkı indirme kısıtlamaları koydu.
Lütfen deneyin:
• Instagram veya TikTok linkleri
• Farklı bir YouTube videosu
• Daha kısa veya eski YouTube videoları""",
    'signin_required': '🔐 YouTube giriş gerektiriyor. Instagram veya TikTok kullanın.',
    'format_unavailable': '📺 Video formatı mevcut değil. Başka video deneyin.'
}

# Progress messages
PROGRESS = {
    'downloading': '⬇️ İndiriliyor: {percentage}% ({size})',
    'processing': '⚙️ İşleniyor...',
    'uploading': '📤 Telegram\'a gönderiliyor: {percentage}%',
    'finalizing': '🎬 Tamamlanıyor...'
}

# Platform names
PLATFORMS = {
    'instagram': 'Instagram',
    'youtube': 'YouTube',
    'tiktok': 'TikTok'
}

# Language selection
LANGUAGE = {
    'select': 'Lütfen dilinizi seçin:',
    'changed': 'Dil Türkçe olarak değiştirildi ✅',
    'flag': '🇹🇷'
}

# File size formatting
def format_size(bytes_size):
    """Format file size in Turkish"""
    if bytes_size is None:
        return "bilinmiyor"
    
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

# Promotional messages
PROMOTIONAL = {
    'groups': '🎭 Daha fazla bot ve hizmet için gruplarımıza katılın:'
}