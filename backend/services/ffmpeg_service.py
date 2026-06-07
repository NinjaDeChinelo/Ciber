"""
FFmpeg Service - Video Processing
Handles video operations: extraction, encoding, effects, merging
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from loguru import logger

from config.settings import settings
from config.constants import VIDEO_QUALITIES, EXPORT_FORMATS, VIDEO_EFFECTS


class FFmpegService:
    """Service for FFmpeg video processing operations"""
    
    def __init__(self):
        """Initialize FFmpeg service"""
        self.ffmpeg_path = settings.FFMPEG_PATH or "ffmpeg"
        self.ffprobe_path = settings.FFMPEG_PATH.replace("ffmpeg", "ffprobe") if settings.FFMPEG_PATH else "ffprobe"
        self._verify_ffmpeg()
    
    def _verify_ffmpeg(self) -> bool:
        """Verify FFmpeg is installed and accessible"""
        try:
            result = subprocess.run(
                [self.ffmpeg_path, "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("✅ FFmpeg found and verified")
                return True
        except Exception as e:
            logger.error(f"❌ FFmpeg not found: {e}")
            return False
        return False
    
    def get_video_info(self, video_path: str) -> Optional[Dict[str, Any]]:
        """Get video metadata using ffprobe"""
        try:
            cmd = [
                self.ffprobe_path,
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration,r_frame_rate",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                stream = data["streams"][0] if data["streams"] else {}
                
                return {
                    "width": stream.get("width", 0),
                    "height": stream.get("height", 0),
                    "duration": float(stream.get("duration", 0)),
                    "fps": self._calculate_fps(stream.get("r_frame_rate", "0/1")),
                    "codec": stream.get("codec_name", "unknown"),
                }
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
        
        return None
    
    @staticmethod
    def _calculate_fps(r_frame_rate: str) -> float:
        """Calculate FPS from frame rate ratio"""
        try:
            num, den = map(int, r_frame_rate.split("/"))
            return num / den if den != 0 else 0
        except:
            return 0
    
    def extract_thumbnail(self, video_path: str, output_path: str, timestamp: str = "00:00:01") -> bool:
        """Extract thumbnail from video at given timestamp"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-ss", timestamp,
                "-vframes", "1",
                "-vf", "scale=160:90",
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"✅ Thumbnail extracted: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error extracting thumbnail: {e}")
        
        return False
    
    def convert_video(
        self,
        input_path: str,
        output_path: str,
        format: str = "mp4",
        resolution: str = "1080p",
        callback=None
    ) -> bool:
        """
        Convert video to specified format and resolution
        
        Args:
            input_path: Input video path
            output_path: Output video path
            format: Output format (mp4, mov, avi, mkv)
            resolution: Target resolution (720p, 1080p, 1440p, 4k)
            callback: Callback function for progress updates (optional)
        """
        try:
            if format not in EXPORT_FORMATS:
                logger.error(f"Unsupported format: {format}")
                return False
            
            if resolution not in VIDEO_QUALITIES:
                logger.error(f"Unsupported resolution: {resolution}")
                return False
            
            quality_info = VIDEO_QUALITIES[resolution]
            codec = EXPORT_FORMATS[format]["codec"]
            
            # Build FFmpeg command
            cmd = [
                self.ffmpeg_path,
                "-i", input_path,
                "-vf", f"scale={quality_info['resolution']}",
                "-c:v", codec,
                "-b:v", quality_info["bitrate"],
                "-c:a", "aac",
                "-b:a", "128k",
                "-progress", "pipe:1",
                "-y",
                output_path
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Parse progress
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                
                if line.startswith("out_time_ms="):
                    # Update progress if callback provided
                    if callback:
                        callback(line)
            
            process.wait(timeout=settings.FFMPEG_TIMEOUT)
            
            if process.returncode == 0:
                logger.info(f"✅ Video converted: {output_path}")
                return True
            else:
                stderr = process.stderr.read()
                logger.error(f"FFmpeg error: {stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg conversion timeout")
            process.kill()
            return False
        except Exception as e:
            logger.error(f"Error converting video: {e}")
            return False
    
    def apply_effects(
        self,
        input_path: str,
        output_path: str,
        effects: List[str]
    ) -> bool:
        """Apply video effects"""
        try:
            filter_chain = ",".join(effects)
            
            cmd = [
                self.ffmpeg_path,
                "-i", input_path,
                "-vf", filter_chain,
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=settings.FFMPEG_TIMEOUT)
            
            if result.returncode == 0:
                logger.info(f"✅ Effects applied: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error applying effects: {e}")
        
        return False
    
    def merge_videos(
        self,
        video_list: List[str],
        output_path: str,
        transition: Optional[str] = None
    ) -> bool:
        """Merge multiple videos with optional transitions"""
        try:
            # Create concat demuxer file
            concat_file = Path(output_path).parent / "concat.txt"
            
            with open(concat_file, "w") as f:
                for video in video_list:
                    f.write(f"file '{video}'\n")
            
            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c", "copy",
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=settings.FFMPEG_TIMEOUT)
            
            # Clean up concat file
            concat_file.unlink()
            
            if result.returncode == 0:
                logger.info(f"✅ Videos merged: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error merging videos: {e}")
        
        return False
    
    def add_audio(
        self,
        video_path: str,
        audio_path: str,
        output_path: str,
        volume: float = 1.0
    ) -> bool:
        """Add audio track to video"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-af", f"volume={volume}",
                "-shortest",
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=settings.FFMPEG_TIMEOUT)
            
            if result.returncode == 0:
                logger.info(f"✅ Audio added: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error adding audio: {e}")
        
        return False
    
    def add_subtitle(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: str
    ) -> bool:
        """Add subtitle to video"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_path,
                "-vf", f"subtitles={subtitle_path}",
                "-c:a", "copy",
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=settings.FFMPEG_TIMEOUT)
            
            if result.returncode == 0:
                logger.info(f"✅ Subtitle added: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error adding subtitle: {e}")
        
        return False
    
    def cut_video(
        self,
        input_path: str,
        output_path: str,
        start_time: str,
        duration: str
    ) -> bool:
        """Cut video segment"""
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", input_path,
                "-ss", start_time,
                "-t", duration,
                "-c", "copy",
                "-y",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=settings.FFMPEG_TIMEOUT)
            
            if result.returncode == 0:
                logger.info(f"✅ Video cut: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error cutting video: {e}")
        
        return False


# Global instance
ffmpeg_service = FFmpegService()
