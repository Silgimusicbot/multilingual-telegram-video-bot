
import time
import glob
import os
import tempfile
import asyncio
from typing import Optional
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import Message
from bot.utils.logger import setup_logger
from bot.utils.decorators import error_handler, track_usage, typing_action
from bot.utils.language_manager import language_manager
from bot.utils.stats_manager import stats_manager
import yt_dlp
import requests
import instaloader


logger = setup_logger(__name__)
youtube_temp_links = {}
class VideoDownloaderPlugin:
    def __init__(self, client: Client):
        self.client = client
        self.name = "Video Downloader"
        self.version = "1.0.0"
        self.description = "Download videos from TikTok, Instagram, and YouTube"

    def register(self):
        self._register_download_handler()
        self._register_youtube_callback()
        logger.info(f"Plugin '{self.name}' registered successfully")

    def _register_download_handler(self):
        def is_video_url(_, __, message):
            if not message.text:
                return False
            text = message.text.strip().lower()
            return any(platform in text for platform in ["tiktok.com", "youtu.be", "youtube.com", "instagram.com"])

        video_url_filter = filters.create(is_video_url)

        @self.client.on_message(filters.private & filters.text & video_url_filter)
        @error_handler
        @track_usage
        @typing_action
        async def handle_video_download(client: Client, message: Message):
            url = message.text.strip()
            user = message.from_user

            logger.info(f"Video downloader received message from {user.id}: {url[:50]}...")
            processing_text = language_manager.get_text(user.id, 'status', 'processing')
            processing_msg = await message.reply(processing_text)

            try:
                if "tiktok.com" in url.lower():
                    downloading_text = language_manager.get_text(user.id, 'status', 'downloading', platform="TikTok")
                    await processing_msg.edit_text(downloading_text)
                    file_path = await self._download_tiktok(url, processing_msg)
                    platform = "TikTok"

                elif "instagram.com" in url.lower():
                    downloading_text = language_manager.get_text(user.id, 'status', 'downloading', platform="Instagram")
                    await processing_msg.edit_text(downloading_text)
                    file_path = await self._download_instagram(url, processing_msg)
                    platform = "Instagram"

                elif "youtu.be" in url.lower() or "youtube.com" in url.lower():
                    youtube_temp_links[message.id] = {
                        "url": url,
                        "user_id": user.id
                    }
                    buttons = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("📹 Video", callback_data=f"yt_video|{message.id}"),
                            InlineKeyboardButton("🎵 MP3", callback_data=f"yt_audio|{message.id}")
                        ]
                    ])
                    await processing_msg.edit_text("🎬 YouTube yükləmə formatını seçin:", reply_markup=buttons)
                    return

                else:
                    not_supported_text = language_manager.get_text(user.id, 'status', 'not_supported')
                    await processing_msg.edit_text(not_supported_text)
                    return

                if file_path and os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    formatted_size = language_manager.format_size(file_size, user.id)
                    video_title = await self._extract_video_title(url, platform)

                    uploading_text = language_manager.get_text(user.id, 'progress', 'uploading', percentage=0)
                    await processing_msg.edit_text(uploading_text)

                    async def upload_progress_callback(current, total):
                        percentage = int((current / total) * 100)
                        progress_bar = language_manager.create_progress_bar(percentage)
                        text = language_manager.get_text(user.id, 'progress', 'uploading', percentage=percentage)
                        if percentage % 10 == 0:
                            try:
                                await processing_msg.edit_text(f"📤 {text}: {progress_bar}\n📁 {formatted_size}")
                            except:
                                pass

                    platform_text = platform.title()
                    promo_text = self._get_promotional_text(user.id)
                    user_lang = language_manager.get_user_language(user.id)

                    if user_lang == 'az':
                        caption = f"📹 {platform_text}dan yükləndi"
                        if video_title:
                            caption += f"\n🎬 {video_title}"
                        caption += f"\n📁 Ölçü: {formatted_size}\n\n{promo_text}"
                    elif user_lang == 'en':
                        caption = f"📹 Downloaded from {platform_text}"
                        if video_title:
                            caption += f"\n🎬 {video_title}"
                        caption += f"\n📁 Size: {formatted_size}\n\n{promo_text}"
                    elif user_lang == 'tr':
                        caption = f"📹 {platform_text}'dan indirildi"
                        if video_title:
                            caption += f"\n🎬 {video_title}"
                        caption += f"\n📁 Boyut: {formatted_size}\n\n{promo_text}"
                    elif user_lang == 'ru':
                        caption = f"📹 Загружено с {platform_text}"
                        if video_title:
                            caption += f"\n🎬 {video_title}"
                        caption += f"\n📁 Размер: {formatted_size}\n\n{promo_text}"
                    else:
                        caption = f"📹 Downloaded from {platform_text}"
                        if video_title:
                            caption += f"\n🎬 {video_title}"
                        caption += f"\n📁 Size: {formatted_size}\n\n{promo_text}"

                    await message.reply_video(
                        video=file_path,
                        caption=caption,
                        progress=upload_progress_callback
                    )

                    stats_manager.add_download(platform.lower())

                    try:
                        os.remove(file_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to cleanup file {file_path}: {cleanup_error}")

                    await processing_msg.delete()
                    await self._notify_admin_download(user, platform, url, video_title)

                    logger.info(f"Successfully downloaded and sent {platform} video for user {message.from_user.id}")
                else:
                    download_failed = language_manager.get_text(user.id, 'status', 'download_failed')
                    await processing_msg.edit_text(download_failed)

            except Exception as e:
                logger.error(f"Video download error for user {message.from_user.id}: {e}", exc_info=True)
                await processing_msg.edit_text(f"❌ Error downloading video: {str(e)}")

    def _register_youtube_callback(self):
        @self.client.on_callback_query()
        async def youtube_format_callback(client, callback_query):
            data = callback_query.data
            if not data.startswith("yt_"):
                return

            try:
               action, msg_id = data.split("|", 1)
               msg_id = int(msg_id)
            except:
                return await callback_query.message.edit_text("❌ Format xətası!")

            video_data = youtube_temp_links.get(msg_id)
            if not video_data:
                return await callback_query.message.edit_text("❌ Keçici məlumat tapılmadı.")

            url = video_data["url"]
            user_id = video_data["user_id"]
            message = callback_query.message

            await callback_query.answer("Yükləmə başlayır...")
            format_type = "mp4" if action == "yt_video" else "mp3"
            downloading_text = language_manager.get_text(user_id, 'status', 'downloading', platform="YouTube")
            await message.edit_text(downloading_text)

            try:
                file_path = await self._download_youtube(url, message, format_type=format_type)

                if file_path and os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    formatted_size = language_manager.format_size(file_size, user_id)
                    video_title = await self._extract_video_title(url, "YouTube")
                    uploading_text = language_manager.get_text(user_id, 'progress', 'uploading', percentage=0)
                    await message.edit_text(uploading_text)

                    async def upload_progress(current, total):
                        percentage = int((current / total) * 100)
                        bar = language_manager.create_progress_bar(percentage)
                        text = language_manager.get_text(user_id, 'progress', 'uploading', percentage=percentage)
                        if percentage % 10 == 0:
                            try:
                                await message.edit_text(f"📤 {text}: {bar}\n📁 {formatted_size}")
                            except:
                                pass

                    await client.send_document(
                        chat_id=message.chat.id,
                        document=file_path,
                        caption=video_title,
                        progress=upload_progress
                    )

                    try:
                        os.remove(file_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to cleanup YouTube file: {cleanup_error}")

                    youtube_temp_links.pop(msg_id, None)

                else:
                    await message.edit_text(f"❌ Yükləmə uğursuz oldu. Fayl tapılmadı.\n`file_path`: {file_path}\n`mövcudluq`: {os.path.exists(file_path) if file_path else 'None'}")

            except Exception as e:
                logger.error(f"YouTube yükləmə xətası: {e}", exc_info=True)
                await message.edit_text(f"❌ Yükləmə uğursuz oldu:\n{str(e)}")
    
    async def _download_tiktok(self, url: str, progress_msg=None) -> Optional[str]:
        """Download TikTok video using yt-dlp with optimized settings."""
        logger.info(f"Starting TikTok download for: {url}")
        try:
            import yt_dlp
            import random
            
            # Create unique temporary filename
            import os
            import time
            temp_dir = tempfile.gettempdir()
            temp_filename = f"tiktok_{int(time.time())}_{os.getpid()}"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            # Random user agents for TikTok
            user_agents = [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            
            # TikTok optimized configuration
            ydl_opts = {
                'format': 'best[ext=mp4]/mp4/best',
                'outtmpl': f'{temp_path}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'user_agent': random.choice(user_agents),
                'http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                },
                'extractor_args': {
                    'tiktok': {
                        'webpage_url_basename': 'video'
                    }
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # Find the actual downloaded file
            import glob
            pattern = f'{temp_path}.*'
            files = glob.glob(pattern)
            
            if files and os.path.exists(files[0]) and os.path.getsize(files[0]) > 0:
                downloaded_file = files[0]
                logger.info(f"TikTok video saved to: {downloaded_file} (size: {os.path.getsize(downloaded_file)} bytes)")
                return downloaded_file
            else:
                logger.error(f"TikTok download failed or file is empty. Found files: {files}")
                return None
                
        except Exception as e:
            logger.error(f"TikTok download error: {e}", exc_info=True)
            return None
    
    async def _download_youtube(self, url: str, format_type="mp4") -> str | None:
        try:
            temp_dir = tempfile.mkdtemp()
            plugin_dir = os.path.dirname(__file__)
            cookie_path = os.path.join(plugin_dir, "cookieyt.txt")

            ydl_opts = {
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                "format": "bestaudio/best" if format_type == "mp3" else "bestvideo+bestaudio/best",
                "merge_output_format": format_type,
                "quiet": True,
            }

            if os.path.exists(cookie_path):
                ydl_opts["cookiefile"] = cookie_path

            file_path = None

            def run_ydl():
                nonlocal file_path
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    if "requested_downloads" in info:
                        file_path = info["requested_downloads"][0]["filepath"]
                    else:
                        file_path = ydl.prepare_filename(info)

            await asyncio.get_event_loop().run_in_executor(None, run_ydl)

            return file_path if file_path and os.path.exists(file_path) else None
        except Exception as e:
            print(f"❌ YouTube yükləmə xətası: {e}")
            return None
            
            
    
    async def _download_instagram(self, url: str, progress_msg=None) -> Optional[str]:
        import os
        import time
        import tempfile
        import glob
        import yt_dlp
        import logging

        logger = logging.getLogger(__name__)

        logger.info(f"Starting Instagram download for: {url}")

        try:
            temp_dir = tempfile.gettempdir()
            temp_filename = f"instagram_{int(time.time())}_{os.getpid()}"
            temp_path = os.path.join(temp_dir, temp_filename)

        # cookies.txt faylının yolu – bu fayl kodla eyni qovluqda olmalıdır
            cookies_path = os.path.join(os.path.dirname(__file__), "cookies.txt")

        # Fayl varsa davam et
            if not os.path.exists(cookies_path):
                logger.error("cookies.txt tapılmadı!")
                return None

            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': f'{temp_path}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'cookies': cookies_path,
            }

        # Videonu yüklə
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        # Yüklənmiş faylı tap
            pattern = f'{temp_path}.*'
            files = glob.glob(pattern)

            if files and os.path.exists(files[0]) and os.path.getsize(files[0]) > 0:
                 downloaded_file = files[0]
                 logger.info(f"Instagram video saved to: {downloaded_file} (size: {os.path.getsize(downloaded_file)} bytes)")
                 return downloaded_file
            else:
                logger.error(f"Instagram download failed or file is empty. Found files: {files}")
                return None

        except Exception as e:
            logger.error(f"Instagram download error: {e}", exc_info=True)
            return None
    
    def _download_instagram_post(self, loader, shortcode):
        """Helper method to download Instagram post."""
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target="")

    async def _extract_video_title(self, url: str, platform: str) -> str:
        """Extract video title from URL."""
        try:
            import random
            
            # TikTok needs special handling
            if "tiktok.com" in url.lower():
                user_agents = [
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
                    'Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
                
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,  # Full extraction needed for TikTok
                    'user_agent': random.choice(user_agents),
                    'http_headers': {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1'
                    }
                }
            else:
                # For YouTube and Instagram
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': True,
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Try multiple title sources
                title = (info.get('title') or 
                        info.get('description', '').split('\n')[0] or
                        info.get('uploader', '') or
                        '')
                
                # Clean and truncate title if too long
                if title:
                    title = title.strip()
                    if len(title) > 100:
                        title = title[:97] + "..."
                    logger.info(f"Extracted {platform} title: {title}")
                    return title
                else:
                    logger.debug(f"No title found for {platform} video")
                    return f"Video by {info.get('uploader', platform)}"
                
        except Exception as e:
            logger.debug(f"Could not extract title from {url}: {e}")
            return ""

    async def _notify_admin_download(self, user, platform: str, url: str, video_title: str = None):
        """Send notification to admin about video download."""
        try:
            from bot.config import config
            import datetime
            import pytz
            
            # Get first admin ID
            admin_id = config.ADMIN_IDS[0] if config.ADMIN_IDS else None
            if not admin_id:
                return
                
            # Get current time in Baku timezone
            baku_tz = pytz.timezone('Asia/Baku')
            current_time = datetime.datetime.now(baku_tz)
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            username = f"@{user.username}" if user.username else "No username"
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            
            # Create admin notification message
            admin_message = f"""📹 **Video Yükləndi**

📅 **Tarix:** {formatted_time}
👤 **İstifadəçi:** {full_name}
🆔 **Username:** {username}
🔢 **ID:** `{user.id}`
🌐 **Platform:** {platform.title()}

📝 **Video Başlığı:** {video_title or 'Məlum deyil'}

🔗 **Orijinal Link:**
{url}"""

            await self.client.send_message(admin_id, admin_message)
            logger.info(f"Download notification sent to admin {admin_id} for user {user.id}")
            
        except Exception as e:
            logger.error(f"Error sending download notification to admin: {e}")

    def _get_promotional_text(self, user_id: int) -> str:
        """Get promotional text for Telegram groups in user's language."""
        from bot.utils.language_manager import language_manager
        
        # Get promotional text in user's language
        promo_text = language_manager.get_text(user_id, 'promotional', 'groups')
        
        # Add the group links
        groups = "@silgiuserbots | @silgiub | @silgiuserbotchat"
        
        return f"{promo_text}\n{groups}"
