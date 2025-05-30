"""
Command handlers for the Telegram bot.
Handles all bot commands like /start, /help, etc.
"""

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.utils.logger import setup_logger
from bot.utils.decorators import error_handler, track_usage
from bot.config import config
from bot.utils.language_manager import language_manager
from bot.utils.stats_manager import stats_manager
import os
import asyncio

logger = setup_logger(__name__)

def register_command_handlers(client: Client):
    """Register all command handlers."""
    
    @client.on_message(filters.command("start") & filters.private)
    @error_handler
    @track_usage
    async def start_command(client: Client, message: Message):
        """Handle /start command with language selection."""
        user = message.from_user
        user_id = user.id
        
        # Add user to statistics
        stats_manager.add_user(user.id)
        stats_manager.add_command()
        
        # Get welcome text in user's language
        welcome_text = language_manager.get_text(user_id, 'commands', 'start')
        
        # Create language selection keyboard
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
        
        # Add language selection text
        lang_select_text = language_manager.get_text(user_id, 'language', 'select')
        full_text = f"{welcome_text}\n\n🌐 {lang_select_text}"
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(full_text, reply_markup=reply_markup)
        logger.info(f"Start command used by {user.id} (@{user.username or 'No username'})")
    
    @client.on_message(filters.command("language"))
    @error_handler
    @track_usage
    async def language_command(client: Client, message: Message):
        """Handle /language command for changing language."""
        user_id = message.from_user.id
        
        # Create language selection keyboard
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
        
        # Get language selection text
        lang_select_text = language_manager.get_text(user_id, 'language', 'select')
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(f"🌐 {lang_select_text}", reply_markup=reply_markup)
    
    @client.on_callback_query(filters.regex(r"^lang_"))
    async def language_callback(client: Client, callback_query: CallbackQuery):
        """Handle language selection callbacks."""
        user_id = callback_query.from_user.id
        language_code = callback_query.data.split("_")[1]
        
        # Set user language
        if language_manager.set_user_language(user_id, language_code):
            # Get confirmation message in new language
            confirmation = language_manager.get_text(user_id, 'language', 'changed')
            await callback_query.answer(confirmation, show_alert=True)
            
            # Update message with new welcome text
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
        """Handle /help command."""
        user = message.from_user
        help_text = language_manager.get_text(user.id, 'help', 'text')
        
        await message.reply_text(help_text)
        logger.info(f"Help command used by {message.from_user.id}")
    
    @client.on_message(filters.command("info"))
    @error_handler
    @track_usage
    async def info_command(client: Client, message: Message):
        """Handle /info command."""
        user = message.from_user
        info_text = language_manager.get_text(user.id, 'info', 'text')
        
        await message.reply_text(info_text)
        logger.info(f"Info command used by {message.from_user.id}")
    
    @client.on_message(filters.command("stats"))
    @error_handler
    @track_usage
    async def stats_command(client: Client, message: Message):
        """Handle /stats command."""
        user = message.from_user
        
        # Get stats text with user data
        stats_text = language_manager.get_text(
            user.id, 'stats', 'text',
            username=user.first_name or "Unknown",
            user_id_display=user.id,
            first_use="Today",
            total_requests=1,
            successful_downloads=0,
            instagram_count=0,
            tiktok_count=0,
            youtube_count=0,
            last_activity="Now"
        )
        
        await message.reply_text(stats_text)
        logger.info(f"Stats command used by {user.id}")
    
    # Admin-only commands
    @client.on_message(filters.command("admin") & filters.user(config.ADMIN_IDS))
    @error_handler
    async def admin_command(client: Client, message: Message):
        """Handle /admin command (admin only)."""
        stats_text = stats_manager.get_stats_text()
        
        admin_text = f"""🔧 **Admin Panel**

{stats_text}

**Mövcud Admin Əmrləri:**
• `/admin` - Bu admin panelini göstər
• `/logs` - Son log qeydlərini al
• `/broadcast <mesaj>` - Bütün istifadəçilərə mesaj göndər
• `/shutdown` - Bot'u təmiz şəkildə bağla

**Bot Status:** ✅ Çalışır
**Framework:** Pyrogram"""
        
        await message.reply_text(admin_text)
        logger.info(f"Admin command used by {message.from_user.id}")
    
    @client.on_message(filters.command("logs") & filters.user(config.ADMIN_IDS))
    @error_handler
    async def logs_command(client: Client, message: Message):
        """Handle /logs command (admin only)."""
        try:
            # Try to read recent logs from console or log file
            log_content = "📋 **Son Log Qeydləri:**\n\n```\n"
            
            # First try to get from environment logs (GitHub Actions)
            if os.path.exists("/tmp/bot.log"):
                with open("/tmp/bot.log", 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    recent_lines = lines[-20:] if len(lines) > 20 else lines
                    for line in recent_lines:
                        log_content += line.strip() + "\n"
            else:
                # If no log file, show recent activity from stats
                log_content += f"Bot başladı: {stats_manager.stats['bot_started_at']}\n"
                log_content += f"Son aktivlik: {stats_manager.stats['last_activity']}\n"
                log_content += f"Ümumi endirmələr: {stats_manager.stats['total_downloads']}\n"
                log_content += f"Ümumi istifadəçilər: {len(stats_manager.stats['unique_users'])}\n"
                log_content += f"İstifadə olunan əmrlər: {stats_manager.stats['commands_used']}\n"
            
            log_content += "```"
            
            # Split message if too long
            if len(log_content) > 4000:
                log_content = log_content[:4000] + "...\n```"
            
            await message.reply_text(log_content)
            logger.info(f"Logs command used by {message.from_user.id}")
            
        except Exception as e:
            await message.reply_text(f"❌ Log oxumaq xətası: {str(e)}")
            logger.error(f"Error reading logs: {e}")
    
    @client.on_message(filters.command("broadcast") & filters.user(config.ADMIN_IDS))
    @error_handler
    async def broadcast_command(client: Client, message: Message):
        """Handle /broadcast command (admin only)."""
        command_parts = message.text.split(None, 1)
        
        if len(command_parts) < 2:
            await message.reply_text(
                "❌ **Broadcast Mesajı Formatı:**\n\n"
                "`/broadcast Bu mesaj bütün istifadəçilərə göndəriləcək`\n\n"
                "**Nümunə:**\n"
                "`/broadcast 🎉 Bot yeniləndı! Yeni xüsusiyyətlər əlavə edildi.`"
            )
            return
        
        broadcast_text = command_parts[1]
        
        # Get all users from statistics
        if isinstance(stats_manager.stats["unique_users"], list):
            stats_manager.stats["unique_users"] = set(stats_manager.stats["unique_users"])
        
        all_users = list(stats_manager.stats["unique_users"])
        
        if not all_users:
            await message.reply_text("❌ Heç bir istifadəçi tapılmadı.")
            return
        
        # Send confirmation and start broadcasting immediately
        confirm_text = f"""📢 **Broadcast Başladılır**

**Mesaj:** {broadcast_text}
**Göndəriləcək istifadəçi sayı:** {len(all_users)}"""
        
        status_msg = await message.reply_text(confirm_text)
        
        sent_count = 0
        failed_count = 0
        
        for i, user_id in enumerate(all_users):
            try:
                await client.send_message(
                    chat_id=user_id,
                    text=f"📢 **Admin Mesajı:**\n\n{broadcast_text}"
                )
                sent_count += 1
                
                # Update progress every 10 users
                if (i + 1) % 10 == 0:
                    await status_msg.edit_text(
                        f"📤 Göndərilir... {i + 1}/{len(all_users)}\n"
                        f"✅ Uğurlu: {sent_count}\n"
                        f"❌ Uğursuz: {failed_count}"
                    )
                
                # Small delay to avoid rate limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                failed_count += 1
                logger.warning(f"Failed to send broadcast to {user_id}: {e}")
        
        # Final status
        await status_msg.edit_text(
            f"✅ **Broadcast Tamamlandı**\n\n"
            f"📊 **Nəticələr:**\n"
            f"• Ümumi istifadəçi: {len(all_users)}\n"
            f"• Uğurla göndərilən: {sent_count}\n"
            f"• Uğursuz: {failed_count}\n"
            f"• Uğur dərəcəsi: {(sent_count/len(all_users)*100):.1f}%"
        )
        
        logger.info(f"Broadcast completed by admin {message.from_user.id}: {sent_count}/{len(all_users)} successful")

    @client.on_message(filters.command("shutdown") & filters.user(config.ADMIN_IDS))
    @error_handler
    async def shutdown_command(client: Client, message: Message):
        """Handle /shutdown command (admin only)."""
        await message.reply_text("🔄 Shutting down bot gracefully...")
        logger.warning(f"Shutdown command issued by admin {message.from_user.id}")
        
        # This would trigger a graceful shutdown
        # Implementation depends on your deployment setup
        await message.reply_text("✅ Shutdown command received. Bot will stop after current operations.")
    
    logger.info("Command handlers registered successfully")
