"""
Utility validators for URLs and files
"""

import re
from typing import Tuple
from pathlib import Path


class URLValidator:
    """Validate URLs for Instagram and other sources"""
    
    # Instagram URL patterns
    INSTAGRAM_PATTERNS = [
        r'(?:https?://)?(?:www\.)?instagram\.com/p/([A-Za-z0-9_-]+)',  # Post
        r'(?:https?://)?(?:www\.)?instagram\.com/reel/([A-Za-z0-9_-]+)',  # Reel
        r'(?:https?://)?(?:www\.)?instagram\.com/tv/([A-Za-z0-9_-]+)',  # IGTV
    ]
    
    @staticmethod
    def validate_instagram_url(url: str) -> Tuple[bool, str]:
        """
        Validate Instagram URL
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not url:
            return False, "URL is empty"
        
        # Check if URL matches Instagram patterns
        for pattern in URLValidator.INSTAGRAM_PATTERNS:
            if re.match(pattern, url):
                return True, "Valid Instagram URL"
        
        return False, "Invalid Instagram URL format"
    
    @staticmethod
    def validate_http_url(url: str) -> Tuple[bool, str]:
        """Validate generic HTTP URL"""
        url_pattern = r'^https?://[^\s]+$'
        
        if re.match(url_pattern, url):
            return True, "Valid URL"
        
        return False, "Invalid URL format"


class FileValidator:
    """Validate files and file paths"""
    
    ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm', '.m4v'}
    ALLOWED_AUDIO_EXTENSIONS = {'.mp3', '.aac', '.wav', '.flac', '.m4a'}
    MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB
    
    @staticmethod
    def validate_video_file(file_path: str) -> Tuple[bool, str]:
        """Validate video file"""
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, f"File not found: {file_path}"
        
        # Check extension
        if path.suffix.lower() not in FileValidator.ALLOWED_VIDEO_EXTENSIONS:
            return False, f"Unsupported video format: {path.suffix}"
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > FileValidator.MAX_FILE_SIZE:
            return False, f"File too large: {file_size / (1024**3):.2f}GB (max 2GB)"
        
        return True, "Valid video file"
    
    @staticmethod
    def validate_audio_file(file_path: str) -> Tuple[bool, str]:
        """Validate audio file"""
        path = Path(file_path)
        
        if not path.exists():
            return False, f"File not found: {file_path}"
        
        if path.suffix.lower() not in FileValidator.ALLOWED_AUDIO_EXTENSIONS:
            return False, f"Unsupported audio format: {path.suffix}"
        
        return True, "Valid audio file"
    
    @staticmethod
    def validate_directory(dir_path: str, create: bool = True) -> Tuple[bool, str]:
        """Validate directory exists or can be created"""
        path = Path(dir_path)
        
        if path.exists():
            if not path.is_dir():
                return False, f"Path exists but is not a directory: {dir_path}"
            return True, "Directory exists"
        
        if create:
            try:
                path.mkdir(parents=True, exist_ok=True)
                return True, f"Directory created: {dir_path}"
            except Exception as e:
                return False, f"Cannot create directory: {e}"
        
        return False, f"Directory does not exist: {dir_path}"


class InputValidator:
    """Validate user inputs"""
    
    @staticmethod
    def validate_text(text: str, min_length: int = 1, max_length: int = 255) -> Tuple[bool, str]:
        """Validate text input"""
        if not text or len(text.strip()) == 0:
            return False, "Text cannot be empty"
        
        if len(text) < min_length:
            return False, f"Text too short (minimum {min_length} characters)"
        
        if len(text) > max_length:
            return False, f"Text too long (maximum {max_length} characters)"
        
        return True, "Valid text"
    
    @staticmethod
    def validate_integer(value: int, min_val: int = None, max_val: int = None) -> Tuple[bool, str]:
        """Validate integer input"""
        if not isinstance(value, int):
            return False, "Value must be an integer"
        
        if min_val is not None and value < min_val:
            return False, f"Value too small (minimum {min_val})"
        
        if max_val is not None and value > max_val:
            return False, f"Value too large (maximum {max_val})"
        
        return True, "Valid integer"
    
    @staticmethod
    def validate_percentage(value: int) -> Tuple[bool, str]:
        """Validate percentage (0-100)"""
        return InputValidator.validate_integer(value, 0, 100)
