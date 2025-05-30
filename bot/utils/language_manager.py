"""
Language management system for multi-language bot support.
"""

import json
import os
from typing import Dict, Optional
from bot.localization import az, en, tr, ru

class LanguageManager:
    """Manages user language preferences and translations."""
    
    def __init__(self):
        self.languages = {
            'az': az,
            'en': en,
            'tr': tr,
            'ru': ru
        }
        self.default_language = 'az'
        self.user_languages = {}
        self.data_file = 'user_languages.json'
        self.load_user_languages()
    
    def load_user_languages(self):
        """Load user language preferences from file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.user_languages = json.load(f)
        except Exception as e:
            print(f"Error loading user languages: {e}")
            self.user_languages = {}
    
    def save_user_languages(self):
        """Save user language preferences to file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_languages, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving user languages: {e}")
    
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language."""
        return self.user_languages.get(str(user_id), self.default_language)
    
    def set_user_language(self, user_id: int, language: str):
        """Set user's preferred language."""
        if language in self.languages:
            self.user_languages[str(user_id)] = language
            self.save_user_languages()
            return True
        return False
    
    def get_text(self, user_id: int, category: str, key: str, **kwargs) -> str:
        """Get translated text for user."""
        lang = self.get_user_language(user_id)
        lang_module = self.languages.get(lang, self.languages[self.default_language])
        
        try:
            # First try to get from TEXTS dictionary
            if hasattr(lang_module, 'TEXTS'):
                texts = getattr(lang_module, 'TEXTS')
                if category in texts and key in texts[category]:
                    text = texts[category][key]
                    if kwargs:
                        return text.format(**kwargs)
                    return text
            
            # Try uppercase attribute names for individual sections
            if hasattr(lang_module, category.upper()):
                text_dict = getattr(lang_module, category.upper())
                text = text_dict.get(key, '')
                
                if isinstance(text, dict):
                    text = text.get('text', '')
                
                # Format text with provided arguments
                if kwargs:
                    return text.format(**kwargs)
                return text
            
            # Language-specific fallback messages based on category and key
            fallback_texts = {
                'az': {
                    'help': {'text': """🤖 Silgi Video Yükləmə Botu

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

⚠️ Qeyd: YouTube platformasında məhdudiyyətlər var."""},
                    'info': {'text': """ℹ️ Bot haqqında

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
Bütün fayllar müvəqqəti saxlanılır və avtomatik silinir."""},
                    'stats': {'text': f"""📊 Statistikalar

👤 İstifadəçi: {kwargs.get('username', 'Bilinmir')}
🆔 ID: {kwargs.get('user_id_display', 'N/A')}
📅 İlk istifadə: {kwargs.get('first_use', 'Bu gün')}
📈 Ümumi sorğular: {kwargs.get('total_requests', 1)}
⬇️ Uğurlu yüklənmələr: {kwargs.get('successful_downloads', 0)}

🏆 Platform statistikaları:
• Instagram: {kwargs.get('instagram_count', 0)}
• TikTok: {kwargs.get('tiktok_count', 0)}
• YouTube: {kwargs.get('youtube_count', 0)}

⚡ Son fəaliyyət: {kwargs.get('last_activity', 'İndi')}"""}
                },
                'en': {
                    'help': {'text': """🤖 Silgi Video Download Bot

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

⚠️ Note: YouTube has restrictions."""},
                    'info': {'text': """ℹ️ About Bot

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
All files are temporarily stored and automatically deleted."""},
                    'stats': {'text': f"""📊 Statistics

👤 User: {kwargs.get('username', 'Unknown')}
🆔 ID: {kwargs.get('user_id_display', 'N/A')}
📅 First use: {kwargs.get('first_use', 'Today')}
📈 Total requests: {kwargs.get('total_requests', 1)}
⬇️ Successful downloads: {kwargs.get('successful_downloads', 0)}

🏆 Platform statistics:
• Instagram: {kwargs.get('instagram_count', 0)}
• TikTok: {kwargs.get('tiktok_count', 0)}
• YouTube: {kwargs.get('youtube_count', 0)}

⚡ Last activity: {kwargs.get('last_activity', 'Now')}"""}
                },
                'tr': {
                    'help': {'text': """🤖 Silgi Video İndirme Botu

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

⚠️ Not: YouTube'da kısıtlamalar var."""},
                    'info': {'text': """ℹ️ Bot Hakkında

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
Tüm dosyalar geçici olarak saklanır ve otomatik silinir."""},
                    'stats': {'text': f"""📊 İstatistikler

👤 Kullanıcı: {kwargs.get('username', 'Bilinmiyor')}
🆔 ID: {kwargs.get('user_id_display', 'N/A')}
📅 İlk kullanım: {kwargs.get('first_use', 'Bugün')}
📈 Toplam istekler: {kwargs.get('total_requests', 1)}
⬇️ Başarılı indirmeler: {kwargs.get('successful_downloads', 0)}

🏆 Platform istatistikleri:
• Instagram: {kwargs.get('instagram_count', 0)}
• TikTok: {kwargs.get('tiktok_count', 0)}
• YouTube: {kwargs.get('youtube_count', 0)}

⚡ Son aktivite: {kwargs.get('last_activity', 'Şimdi')}"""}
                },
                'ru': {
                    'help': {'text': """🤖 Silgi Video Download Bot

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

⚠️ Примечание: YouTube имеет ограничения."""},
                    'info': {'text': """ℹ️ О боте

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
Все файлы временно хранятся и автоматически удаляются."""},
                    'stats': {'text': f"""📊 Статистика

👤 Пользователь: {kwargs.get('username', 'Неизвестно')}
🆔 ID: {kwargs.get('user_id_display', 'N/A')}
📅 Первое использование: {kwargs.get('first_use', 'Сегодня')}
📈 Всего запросов: {kwargs.get('total_requests', 1)}
⬇️ Успешных загрузок: {kwargs.get('successful_downloads', 0)}

🏆 Статистика по платформам:
• Instagram: {kwargs.get('instagram_count', 0)}
• TikTok: {kwargs.get('tiktok_count', 0)}
• YouTube: {kwargs.get('youtube_count', 0)}

⚡ Последняя активность: {kwargs.get('last_activity', 'Сейчас')}"""}
                }
            }
            
            # Use language-specific fallback
            if lang in fallback_texts and category in fallback_texts[lang] and key in fallback_texts[lang][category]:
                text = fallback_texts[lang][category][key]
                if isinstance(text, dict):
                    text = text.get('text', '')
                return text
            
            # Default English fallback
            if 'en' in fallback_texts and category in fallback_texts['en'] and key in fallback_texts['en'][category]:
                text = fallback_texts['en'][category][key]
                if isinstance(text, dict):
                    text = text.get('text', '')
                return text
            
            return f"Text not found: {category}.{key}"
        except Exception as e:
            print(f"Error getting text for {lang}.{category}.{key}: {e}")
            return f"Error: {category}.{key}"
    
    def get_language_info(self, language: str) -> Dict:
        """Get language information."""
        lang_info = {
            'az': {'name': 'Azərbaycan', 'flag': '🇦🇿'},
            'en': {'name': 'English', 'flag': '🇺🇸'},
            'tr': {'name': 'Türkçe', 'flag': '🇹🇷'},
            'ru': {'name': 'Русский', 'flag': '🇷🇺'}
        }
        return lang_info.get(language, lang_info['az'])
    
    def get_available_languages(self) -> Dict:
        """Get all available languages."""
        return {
            'az': {'name': 'Azərbaycan', 'flag': '🇦🇿'},
            'en': {'name': 'English', 'flag': '🇺🇸'},
            'tr': {'name': 'Türkçe', 'flag': '🇹🇷'},
            'ru': {'name': 'Русский', 'flag': '🇷🇺'}
        }
    
    def format_size(self, bytes_size, user_id: int = None):
        """Format file size in user's language."""
        if bytes_size is None:
            lang = self.get_user_language(user_id or 0)
            if lang == 'ru':
                return "неизвестно"
            elif lang == 'tr':
                return "bilinmiyor"
            elif lang == 'az':
                return "bilinmir"
            else:
                return "unknown"
        
        for unit in ['bytes', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    
    def create_progress_bar(self, percentage, length=10):
        """Create visual progress bar."""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] {percentage}%"

# Global instance
language_manager = LanguageManager()