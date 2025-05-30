"""
Russian localization for the Telegram bot.
"""

# Command messages
COMMANDS = {
    'start': {
        'text': """👋 Привет! Я бот для скачивания видео.

📱 Поддерживаемые платформы:
• Instagram (Reels, Posts, Stories)
• TikTok видео
• YouTube видео (ограничено)

📋 Основные команды:
/help - Справка
/info - Информация о боте
/stats - Статистика
/language - Изменить язык

🔗 Отправьте мне ссылку на видео, и я скачаю его для вас!"""
    },
    'help': {
        'text': """❓ Справочная информация

🎯 Как работает бот:
1. Отправьте ссылку на видео
2. Бот обработает видео
3. Видео будет отправлено вам

📱 Поддерживаемые платформы:
• Instagram - Полная поддержка
• TikTok - Полная поддержка
• YouTube - Ограниченная поддержка

💡 Советы:
• Используйте полные ссылки вместо коротких (youtu.be)
• Видео из приватных аккаунтов могут быть недоступны
• Большие файлы могут загружаться дольше

❌ Проблемы:
Если возникают проблемы, попробуйте другую ссылку или обратитесь к администратору."""
    },
    'info': {
        'text': """ℹ️ О боте

🤖 Название: Silgi Video Downloader Bot
🔧 Версия: 2.0.0
⚡ Технология: Pyrogram + yt-dlp

🌟 Особенности:
• Быстрое скачивание видео
• Поддержка множества платформ
• Индикатор прогресса загрузки
• Автоматическая очистка файлов

📊 Производительность:
• Instagram: Отлично
• TikTok: Отлично
• YouTube: Ограничено

🛡️ Безопасность:
Все файлы временно хранятся и автоматически удаляются."""
    },
    'help': {
        'text': """🤖 Silgi Video Download Bot

📥 Поддерживаемые платформы:
• Instagram (Reels, видео)
• TikTok (видео) 
• YouTube (ограниченно)

🔧 Команды:
/start - Запустить бота и выбрать язык
/help - Это сообщение помощи
/info - Информация о боте
/stats - Статистика использования
/language - Изменить язык

📝 Использование:
Отправьте ссылку на видео, и бот автоматически загрузит его.

⚠️ Примечание: YouTube имеет ограничения."""
    },
    'info': {
        'text': """ℹ️ О боте

🤖 Название: Silgi Video Download Bot
🔧 Версия: 2.0.0
⚡ Технология: Pyrogram + yt-dlp

🌟 Возможности:
• Быстрая загрузка видео
• Поддержка нескольких платформ
• Индикаторы прогресса загрузки
• Автоматическая очистка файлов

📊 Производительность:
• Instagram: Отлично
• TikTok: Отлично
• YouTube: Ограниченно

🛡️ Безопасность:
Все файлы временно хранятся и автоматически удаляются."""
    },
    'stats': {
        'text': """📊 Статистика

👤 Пользователь: {username}
🆔 ID: {user_id}
📅 Первое использование: {first_use}
📈 Всего запросов: {total_requests}
⬇️ Успешных загрузок: {successful_downloads}

🏆 Статистика по платформам:
• Instagram: {instagram_count}
• TikTok: {tiktok_count}
• YouTube: {youtube_count}

⚡ Последняя активность: {last_activity}"""
    }
}

# Status messages
STATUS = {
    'processing': '🔄 Обработка ссылки на видео...',
    'downloading': '⬇️ Загрузка видео ({platform})...',
    'uploading': '📤 Отправка видео...',
    'success': '✅ Видео успешно отправлено!',
    'error': '❌ Произошла ошибка: {error}',
    'not_supported': '❌ Эта ссылка не поддерживается. Отправьте ссылку Instagram, TikTok или YouTube.',
    'invalid_link': '❌ Неверный формат ссылки. Отправьте правильную ссылку на видео.',
    'file_too_large': '❌ Файл слишком большой. Попробуйте видео поменьше.',
    'download_failed': '❌ Не удалось скачать видео. Проверьте ссылку и попробуйте снова.'
}

# YouTube specific messages
YOUTUBE = {
    'restrictions': """⚠️ YouTube установил строгие ограничения на загрузку.
Пожалуйста, попробуйте:
• Ссылки Instagram или TikTok
• Другое видео YouTube
• Более короткие или старые видео YouTube""",
    'signin_required': '🔐 YouTube требует входа в систему. Используйте Instagram или TikTok.',
    'format_unavailable': '📺 Формат видео недоступен. Попробуйте другое видео.'
}

# Progress messages
PROGRESS = {
    'downloading': '⬇️ Загрузка: {percentage}% ({size})',
    'processing': '⚙️ Обработка...',
    'uploading': '📤 Отправка в Telegram: {percentage}%',
    'finalizing': '🎬 Завершение...'
}

# Platform names
PLATFORMS = {
    'instagram': 'Instagram',
    'youtube': 'YouTube',
    'tiktok': 'TikTok'
}

# Language selection
LANGUAGE = {
    'select': 'Пожалуйста, выберите ваш язык:',
    'changed': 'Язык изменен на русский ✅',
    'flag': '🇷🇺'
}

# File size formatting
def format_size(bytes_size):
    """Format file size in Russian"""
    if bytes_size is None:
        return "неизвестно"
    
    for unit in ['байт', 'КБ', 'МБ', 'ГБ']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} ТБ"

def create_progress_bar(percentage, length=10):
    """Create visual progress bar"""
    filled = int(length * percentage / 100)
    bar = '█' * filled + '░' * (length - filled)
    return f"[{bar}] {percentage}%"

# Promotional messages
PROMOTIONAL = {
    'groups': '🎭 Присоединяйтесь к нашим группам для получения дополнительных ботов и услуг:'
}