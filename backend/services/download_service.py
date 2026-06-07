"""
Download Service - Manage video downloads
"""

import asyncio
import aiohttp
from pathlib import Path
from typing import Optional, Callable, List
from datetime import datetime
from loguru import logger

from config.settings import settings
from config.database import SessionLocal
from models.models import DownloadQueue, Video
from services.ffmpeg_service import ffmpeg_service


class DownloadService:
    """Service for managing video downloads"""
    
    def __init__(self):
        """Initialize download service"""
        self.active_downloads: dict = {}
        self.max_concurrent = settings.MAX_CONCURRENT_DOWNLOADS
        self.chunk_size = settings.DOWNLOAD_CHUNK_SIZE
        self.timeout = aiohttp.ClientTimeout(total=settings.DOWNLOAD_TIMEOUT)
    
    async def download_video(
        self,
        url: str,
        output_path: str,
        progress_callback: Optional[Callable] = None,
        download_id: Optional[int] = None
    ) -> bool:
        """
        Download video from URL with progress tracking
        
        Args:
            url: Video URL
            output_path: Output file path
            progress_callback: Callback function for progress updates
            download_id: Download queue item ID
        """
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, ssl=False) as response:
                    if response.status != 200:
                        logger.error(f"Download failed with status {response.status}")
                        return False
                    
                    total_size = int(response.headers.get("content-length", 0))
                    downloaded = 0
                    
                    # Create output directory
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(output_path, "wb") as f:
                        async for chunk in response.content.iter_chunked(self.chunk_size):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                
                                # Calculate progress
                                if total_size > 0:
                                    progress = (downloaded / total_size) * 100
                                    
                                    if progress_callback:
                                        await progress_callback(progress, downloaded, total_size)
                                    
                                    # Update database
                                    if download_id:
                                        self._update_download_progress(download_id, progress, downloaded)
                    
                    logger.info(f"✅ Download completed: {output_path}")
                    
                    # Extract thumbnail
                    self._extract_thumbnail(output_path)
                    
                    return True
                    
        except asyncio.TimeoutError:
            logger.error("Download timeout")
        except Exception as e:
            logger.error(f"Download error: {e}")
        
        return False
    
    async def download_batch(
        self,
        urls: List[str],
        progress_callback: Optional[Callable] = None
    ) -> dict:
        """
        Download multiple videos concurrently
        
        Args:
            urls: List of video URLs
            progress_callback: Callback for progress updates
            
        Returns:
            Dictionary with results
        """
        results = {
            "total": len(urls),
            "successful": 0,
            "failed": 0,
            "downloads": []
        }
        
        # Create semaphore to limit concurrent downloads
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def download_with_semaphore(url: str):
            async with semaphore:
                output_path = settings.VIDEOS_DIR / self._generate_filename(url)
                success = await self.download_video(
                    url,
                    str(output_path),
                    progress_callback
                )
                
                if success:
                    results["successful"] += 1
                    results["downloads"].append({
                        "url": url,
                        "path": str(output_path),
                        "status": "completed"
                    })
                else:
                    results["failed"] += 1
                    results["downloads"].append({
                        "url": url,
                        "status": "failed"
                    })
        
        # Run downloads concurrently
        tasks = [download_with_semaphore(url) for url in urls]
        await asyncio.gather(*tasks)
        
        logger.info(f"Batch download completed: {results['successful']}/{results['total']} successful")
        return results
    
    @staticmethod
    def _generate_filename(url: str) -> str:
        """Generate unique filename from URL"""
        from urllib.parse import urlparse
        import hashlib
        
        parsed = urlparse(url)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        return f"video_{timestamp}_{url_hash}.mp4"
    
    def _update_download_progress(self, download_id: int, progress: float, downloaded: int):
        """Update download progress in database"""
        try:
            db = SessionLocal()
            download = db.query(DownloadQueue).filter(DownloadQueue.id == download_id).first()
            
            if download:
                download.progress = min(100, int(progress))
                download.downloaded_size = downloaded
                if progress >= 100:
                    download.status = "completed"
                    download.completed_at = datetime.utcnow()
                
                db.commit()
        except Exception as e:
            logger.error(f"Error updating download progress: {e}")
        finally:
            db.close()
    
    @staticmethod
    def _extract_thumbnail(video_path: str):
        """Extract thumbnail for downloaded video"""
        try:
            thumbnail_path = Path(video_path).parent / f"{Path(video_path).stem}_thumb.jpg"
            ffmpeg_service.extract_thumbnail(video_path, str(thumbnail_path))
        except Exception as e:
            logger.warning(f"Could not extract thumbnail: {e}")
    
    def pause_download(self, download_id: int):
        """Pause an active download"""
        try:
            db = SessionLocal()
            download = db.query(DownloadQueue).filter(DownloadQueue.id == download_id).first()
            
            if download:
                download.status = "paused"
                db.commit()
                logger.info(f"Download {download_id} paused")
        except Exception as e:
            logger.error(f"Error pausing download: {e}")
        finally:
            db.close()
    
    def resume_download(self, download_id: int):
        """Resume a paused download"""
        try:
            db = SessionLocal()
            download = db.query(DownloadQueue).filter(DownloadQueue.id == download_id).first()
            
            if download:
                download.status = "pending"
                db.commit()
                logger.info(f"Download {download_id} resumed")
        except Exception as e:
            logger.error(f"Error resuming download: {e}")
        finally:
            db.close()
    
    def cancel_download(self, download_id: int):
        """Cancel a download"""
        try:
            db = SessionLocal()
            download = db.query(DownloadQueue).filter(DownloadQueue.id == download_id).first()
            
            if download:
                download.status = "cancelled"
                db.commit()
                logger.info(f"Download {download_id} cancelled")
        except Exception as e:
            logger.error(f"Error cancelling download: {e}")
        finally:
            db.close()


# Global instance
download_service = DownloadService()
