
import os
import tempfile
import asyncio
from typing import Optional
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from bot.utils.logger import setup_logger
from bot.utils.decorators import error_handler, track_usage, typing_action
from bot.utils.language_manager import language_manager
from bot.utils.stats_manager import stats_manager
import yt_dlp
import requests
import instaloader
import asyncio

logger = setup_logger(__name__)

class VideoDownloaderPlugin:
    """Plugin for downloading videos from various platforms."""
    
    def __init__(self, client: Client):
        self.client = client
        self.name = "Video Downloader"
        self.version = "1.0.0"
        self.description = "Download videos from TikTok, Instagram, and YouTube"
    
    def register(self):
        """Register all plugin commands."""
        self._register_download_handler()
        logger.info(f"Plugin '{self.name}' registered successfully")
    
    def _register_download_handler(self):
        """Register the video download handler."""
        
        # Create a custom filter for video URLs only
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
            """Handle video download requests."""
            url = message.text.strip()
            user = message.from_user
            
            # Log all text messages received by video downloader
            logger.info(f"Video downloader received message from {user.id}: {url[:50]}...")
            
            # Check if the message contains a supported video platform URL
            supported_platforms = ["tiktok.com", "youtu.be", "youtube.com", "instagram.com"]
            
            # This should not happen with the new filter, but keep as safety check
            if not any(platform in url.lower() for platform in supported_platforms):
                logger.info(f"URL filter missed this, skipping: {url[:30]}...")
                return
            
            logger.info(f"Processing video URL: {url}")
            
            # Send processing message in user's language
            processing_text = language_manager.get_text(user.id, 'status', 'processing')
            processing_msg = await message.reply(processing_text)
            
            try:
                if "tiktok.com" in url.lower():
                    logger.info(f"Attempting TikTok download for: {url}")
                    platform_name = language_manager.get_text(user.id, 'platforms', 'tiktok')
                    downloading_text = language_manager.get_text(user.id, 'status', 'downloading', platform=platform_name)
                    await processing_msg.edit_text(downloading_text)
                    file_path = await self._download_tiktok(url, processing_msg)
                    platform = "TikTok"
                elif "youtu.be" in url.lower() or "youtube.com" in url.lower():
                    logger.info(f"Attempting YouTube download for: {url}")
                    platform_name = language_manager.get_text(user.id, 'platforms', 'youtube')
                    downloading_text = language_manager.get_text(user.id, 'status', 'downloading', platform=platform_name)
                    await processing_msg.edit_text(downloading_text)
                    file_path = await self._download_youtube(url, processing_msg)
                    platform = "YouTube"
                elif "instagram.com" in url.lower():
                    logger.info(f"Attempting Instagram download for: {url}")
                    platform_name = language_manager.get_text(user.id, 'platforms', 'instagram')
                    downloading_text = language_manager.get_text(user.id, 'status', 'downloading', platform=platform_name)
                    await processing_msg.edit_text(downloading_text)
                    file_path = await self._download_instagram(url, processing_msg)
                    platform = "Instagram"
                else:
                    logger.warning(f"Unsupported platform for URL: {url}")
                    not_supported_text = language_manager.get_text(user.id, 'status', 'not_supported')
                    await processing_msg.edit_text(not_supported_text)
                    return
                
                logger.info(f"Download result for {platform}: {file_path}")
                
                if file_path and os.path.exists(file_path):
                    # Get file size for upload progress
                    file_size = os.path.getsize(file_path)
                    formatted_size = language_manager.format_size(file_size, user.id)
                    
                    # Extract video title
                    video_title = await self._extract_video_title(url, platform)
                    
                    # Update status to uploading with progress
                    uploading_text = language_manager.get_text(user.id, 'progress', 'uploading', percentage=0)
                    await processing_msg.edit_text(uploading_text)
                    
                    # Send the video with upload tracking
                    async def upload_progress_callback(current, total):
                        percentage = int((current / total) * 100)
                        progress_bar = language_manager.create_progress_bar(percentage)
                        uploading_text = language_manager.get_text(user.id, 'progress', 'uploading', percentage=percentage)
                        progress_text = f"📤 {uploading_text}: {progress_bar}\n📁 {formatted_size}"
                        try:
                            if percentage % 10 == 0:  # Update every 10%
                                await processing_msg.edit_text(progress_text)
                        except:
                            pass
                    
                    # Create caption with title and promotional message
                    platform_text = platform.title()  # Instagram, TikTok, etc.
                    promo_text = self._get_promotional_text(user.id)
                    
                    # Get user's language for the caption
                    user_lang = language_manager.get_user_language(user.id)
                    
                    # Create localized caption based on user's language
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
                        # Default to English
                        caption = f"📹 Downloaded from {platform_text}"
                        if video_title:
                            caption += f"\n🎬 {video_title}"
                        caption += f"\n📁 Size: {formatted_size}\n\n{promo_text}"
                    
                    await message.reply_video(
                        video=file_path,
                        caption=caption,
                        progress=upload_progress_callback
                    )
                    
                    # Add download to statistics
                    stats_manager.add_download(platform.lower())
                    
                    # Clean up the file
                    try:
                        os.remove(file_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to cleanup file {file_path}: {cleanup_error}")
                    
                    # Delete the processing message
                    await processing_msg.delete()
                    
                    # Send notification to admin about the download
                    await self._notify_admin_download(user, platform, url, video_title)
                    
                    logger.info(f"Successfully downloaded and sent {platform} video for user {message.from_user.id}")
                else:
                    if "youtube" in platform.lower():
                        youtube_error = language_manager.get_text(user.id, 'youtube', 'restrictions')
                        await processing_msg.edit_text(youtube_error)
                    else:
                        download_failed = language_manager.get_text(user.id, 'status', 'download_failed')
                        await processing_msg.edit_text(download_failed)
                    
            except Exception as e:
                logger.error(f"Video download error for user {message.from_user.id}: {e}", exc_info=True)
                await processing_msg.edit_text(f"❌ Error downloading video: {str(e)}")
    
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
    
    async def _download_youtube(self, url: str, progress_msg=None) -> Optional[str]:
        """Download YouTube video using yt-dlp with advanced bypass techniques."""
        logger.info(f"Starting YouTube download for: {url}")
        try:
            import yt_dlp
            import random
            
            # Create unique temporary filename
            import os
            import time
            temp_dir = tempfile.gettempdir()
            temp_filename = f"youtube_{int(time.time())}_{os.getpid()}"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            # Random user agents to avoid detection
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
            ]
            
            # Base configuration
            base_opts = {
                'outtmpl': f'{temp_path}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,
                'embed_subs': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'user_agent': random.choice(user_agents),
                'http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0'
                }
            }
            
            # Advanced YouTube extraction strategies
            extraction_methods = [
                # Method 1: Mobile web client (often bypasses restrictions)
                {
                    **base_opts,
                    'format': '18/mp4[height<=360]/best[height<=360]',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['mweb'],
                            'skip': ['dash', 'hls'],
                            'lang': ['en'],
                            'region': 'US'
                        }
                    },
                    'http_headers': {
                        **base_opts['http_headers'],
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
                    }
                },
                # Method 2: Android TV client (less restricted)
                {
                    **base_opts,
                    'format': 'mp4[height<=480]/18/mp4',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android_tv'],
                            'skip': ['dash', 'hls']
                        }
                    }
                },
                # Method 3: iOS with specific format
                {
                    **base_opts,
                    'format': '22/18/mp4[height<=720]/best[height<=720]',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['ios_music'],
                            'skip': ['dash', 'hls']
                        }
                    },
                    'http_headers': {
                        **base_opts['http_headers'],
                        'User-Agent': 'com.google.ios.youtube/17.33.2 (iPhone14,3; U; CPU iOS 15_6 like Mac OS X)'
                    }
                },
                # Method 4: Embedded player (sometimes works)
                {
                    **base_opts,
                    'format': 'worst[ext=mp4]/mp4/best[height<=360]',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['tv_embedded'],
                            'skip': ['dash', 'hls']
                        }
                    },
                    'http_headers': {
                        **base_opts['http_headers'],
                        'Referer': 'https://www.youtube.com/embed/',
                        'Origin': 'https://www.youtube.com'
                    }
                },
                # Method 5: Age-gated bypass
                {
                    **base_opts,
                    'format': '18/mp4',
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android_agegate'],
                            'skip': ['dash', 'hls']
                        }
                    }
                },
                # Method 6: Audio-only as fallback (convert to video)
                {
                    **base_opts,
                    'format': 'bestaudio[ext=m4a]/bestaudio',
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android'],
                            'skip': ['dash', 'hls']
                        }
                    }
                }
            ]
            
            for i, opts in enumerate(extraction_methods):
                try:
                    logger.info(f"Attempting YouTube extraction method {i+1}")
                    
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        # Add some delay between attempts
                        if i > 0:
                            await asyncio.sleep(2)
                            
                        ydl.download([url])
                        
                    # Find the actual downloaded file
                    import glob
                    pattern = f'{temp_path}.*'
                    files = glob.glob(pattern)
                    
                    if files and os.path.exists(files[0]) and os.path.getsize(files[0]) > 0:
                        downloaded_file = files[0]
                        logger.info(f"YouTube video saved to: {downloaded_file} (size: {os.path.getsize(downloaded_file)} bytes)")
                        return downloaded_file
                        
                except Exception as method_error:
                    logger.warning(f"YouTube extraction method {i+1} failed: {method_error}")
                    # Clean up any partial downloads
                    import glob
                    for partial_file in glob.glob(f'{temp_path}*'):
                        try:
                            os.remove(partial_file)
                        except:
                            pass
                    continue
            
            logger.error(f"All YouTube extraction methods failed")
            return None
                
        except Exception as e:
            logger.error(f"YouTube download error: {e}")
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
