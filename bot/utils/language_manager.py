import json
import os
from typing import Dict, Optional
from bot.localization import az, en, tr, ru

class LanguageManager:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.user_languages = json.load(f)
        except Exception as e:
            print(f"Error loading user languages: {e}")
            self.user_languages = {}
    
    def save_user_languages(self):
        return self.user_languages.get(str(user_id), self.default_language)
    
    def set_user_language(self, user_id: int, language: str):
        lang = self.get_user_language(user_id)
        lang_module = self.languages.get(lang, self.languages[self.default_language])
        
        try:
            if hasattr(lang_module, 'TEXTS'):
                texts = getattr(lang_module, 'TEXTS')
                if category in texts and key in texts[category]:
                    text = texts[category][key]
                    if kwargs:
                        return text.format(**kwargs)
                    return text
            
            if hasattr(lang_module, category.upper()):
                text_dict = getattr(lang_module, category.upper())
                text = text_dict.get(key, '')
                
                if isinstance(text, dict):
                    text = text.get('text', '')
                
                if kwargs:
                    return text.format(**kwargs)
                return text
            
            fallback_texts = {
                'az': {
                },
                'en': {
                },
                'tr': {
                },
                'ru': {
                }
            }
            
            if lang in fallback_texts and category in fallback_texts[lang] and key in fallback_texts[lang][category]:
                text = fallback_texts[lang][category][key]
                if isinstance(text, dict):
                    text = text.get('text', '')
                return text
            
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
        return {
            'az': {'name': 'Azərbaycan', 'flag': '🇦🇿'},
            'en': {'name': 'English', 'flag': '🇺🇸'},
            'tr': {'name': 'Türkçe', 'flag': '🇹🇷'},
            'ru': {'name': 'Русский', 'flag': '🇷🇺'}
        }
    
    def format_size(self, bytes_size, user_id: int = None):
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] {percentage}%"

language_manager = LanguageManager()