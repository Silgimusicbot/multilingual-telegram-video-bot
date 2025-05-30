from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.utils.logger import setup_logger
from bot.utils.decorators import error_handler, track_usage
from bot.config import config
from bot.utils.language_manager import language_manager

logger = setup_logger(__name__)

def register_command_handlers(client: Client):
        user = message.from_user
        user_id = user.id
        
        welcome_text = language_manager.get_text(user_id, 'commands', 'start')
        
        languages = language_manager.get_available_languages()
        keyboard = []
        row = []
        for lang_code, lang_info in languages.items():
            button_text = f"{lang_info['flag']} {lang_info['name']}"
            row.append(InlineKeyboardButton(button_text, callback_data=f"lang_{lang_code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        lang_select_text = language_manager.get_text(user_id, 'language', 'select')
        full_text = f"{welcome_text}\n\n🌐 {lang_select_text}"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(full_text, reply_markup=reply_markup)
        logger.info(f"Start command used by {user.id} (@{user.username or 'No username'})")
    
    @client.on_message(filters.command("language"))
    @error_handler
    @track_usage
    async def language_command(client: Client, message: Message):
        user_id = callback_query.from_user.id
        language_code = callback_query.data.split("_")[1]
        
        if language_manager.set_user_language(user_id, language_code):
            confirmation = language_manager.get_text(user_id, 'language', 'changed')
            await callback_query.answer(confirmation, show_alert=True)
            
            welcome_text = language_manager.get_text(user_id, 'commands', 'start')
            lang_select_text = language_manager.get_text(user_id, 'language', 'select')
            full_text = f"{welcome_text}\n\n🌐 {lang_select_text}"
            
            await callback_query.edit_message_text(full_text, reply_markup=callback_query.message.reply_markup)
        else:
            await callback_query.answer("Error setting language", show_alert=True)
    
    @client.on_message(filters.command("help"))
    @error_handler
    @track_usage
    async def help_command(client: Client, message: Message):
        user = message.from_user
        info_text = language_manager.get_text(user.id, 'info', 'text')
        
        await message.reply_text(info_text)
        logger.info(f"Info command used by {message.from_user.id}")
    
    @client.on_message(filters.command("stats"))
    @error_handler
    @track_usage
    async def stats_command(client: Client, message: Message):
        admin_text = (
            "🔧 **Admin Panel**\n\n"
            "**Available Admin Commands:**\n"
            "• `/admin` - Show this admin panel\n"
            "• `/broadcast <message>` - Send message to all users\n"
            "• `/logs` - Get recent log entries\n"
            "• `/shutdown` - Gracefully shutdown the bot\n\n"
            "**Bot Status:** ✅ Running\n"
            "**Framework:** Pyrogram\n"
            "**Registered Handlers:** Active"
        )
        
        await message.reply_text(admin_text)
        logger.info(f"Admin command used by {message.from_user.id}")
    
    @client.on_message(filters.command("shutdown") & filters.user(config.ADMIN_IDS))
    @error_handler
    async def shutdown_command(client: Client, message: Message):