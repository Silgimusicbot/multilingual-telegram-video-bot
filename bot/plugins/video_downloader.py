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
import yt_dlp
import requests
import instaloader
import asyncio

logger = setup_logger(__name__)

class VideoDownloaderPlugin:
        self._register_download_handler()
        logger.info(f"Plugin '{self.name}' registered successfully")
    
    def _register_download_handler(self):
            url = message.text.strip()
            user = message.from_user
            
            logger.info(f"Video downloader received message from {user.id}: {url[:50]}...")
            
            supported_platforms = ["tiktok.com", "youtu.be", "youtube.com", "instagram.com"]
            
            if not any(platform in url.lower() for platform in supported_platforms):
                logger.info(f"Not a video URL, skipping: {url[:30]}...")
                return
            
            logger.info(f"Processing video URL: {url}")
            
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
                    file_size = os.path.getsize(file_path)
                    formatted_size = language_manager.format_size(file_size, user.id)
                    
                    video_title = await self._extract_video_title(url, platform)
                    
                    uploading_text = language_manager.get_text(user.id, 'progress', 'uploading', percentage=0)
                    await processing_msg.edit_text(uploading_text)
                    
                    async def upload_progress_callback(current, total):
                        percentage = int((current / total) * 100)
                        progress_bar = language_manager.create_progress_bar(percentage)
                        uploading_text = language_manager.get_text(user.id, 'progress', 'uploading', percentage=percentage)
                        progress_text = f"📤 {uploading_text}: {progress_bar}\n📁 {formatted_size}"
                        try:
                            if percentage % 10 == 0:
                                await processing_msg.edit_text(progress_text)
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
                    
                    try:
                        os.remove(file_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to cleanup file {file_path}: {cleanup_error}")
                    
                    await processing_msg.delete()
                    
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
        logger.info(f"Starting YouTube download for: {url}")
        try:
            import yt_dlp
            import random
            
            import os
            import time
            temp_dir = tempfile.gettempdir()
            temp_filename = f"youtube_{int(time.time())}_{os.getpid()}"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
            ]
            
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
            
            extraction_methods = [
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
                        if i > 0:
                            await asyncio.sleep(2)
                            
                        ydl.download([url])
                        
                    import glob
                    pattern = f'{temp_path}.*'
                    files = glob.glob(pattern)
                    
                    if files and os.path.exists(files[0]) and os.path.getsize(files[0]) > 0:
                        downloaded_file = files[0]
                        logger.info(f"YouTube video saved to: {downloaded_file} (size: {os.path.getsize(downloaded_file)} bytes)")
                        return downloaded_file
                        
                except Exception as method_error:
                    logger.warning(f"YouTube extraction method {i+1} failed: {method_error}")
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
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        loader.download_post(post, target="")

    async def _extract_video_title(self, url: str, platform: str) -> str:
        from bot.utils.language_manager import language_manager
        
        promo_text = language_manager.get_text(user_id, 'promotional', 'groups')
        
        groups = "@silgiuserbots | @silgiub | @silgiuserbotchat"
        
        return f"{promo_text}\n{groups}"