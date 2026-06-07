"""
Example code snippets for InstaVideo Studio API usage
"""

# ============ DOWNLOAD SERVICE EXAMPLE ============

import asyncio
from backend.services.download_service import download_service

async def example_single_download():
    """Example: Download single video"""
    url = "https://www.instagram.com/p/ABC123XYZ/"
    output_path = "/path/to/video.mp4"
    
    async def progress_callback(progress):
        print(f"Download progress: {progress:.1f}%")
    
    success = await download_service.download_video(
        url=url,
        output_path=output_path,
        progress_callback=progress_callback
    )
    
    if success:
        print("✅ Download completed!")
    else:
        print("❌ Download failed!")


async def example_batch_download():
    """Example: Download multiple videos"""
    urls = [
        "https://www.instagram.com/p/ABC123XYZ/",
        "https://www.instagram.com/reel/DEF456UVW/",
        "https://www.instagram.com/tv/GHI789RST/",
    ]
    
    results = await download_service.download_batch(urls)
    
    print(f"✅ Successful: {results['successful']}/{results['total']}")
    print(f"❌ Failed: {results['failed']}/{results['total']}")


# ============ FFMPEG SERVICE EXAMPLE ============

from backend.services.ffmpeg_service import ffmpeg_service

def example_get_video_info():
    """Example: Get video metadata"""
    video_path = "/path/to/video.mp4"
    
    info = ffmpeg_service.get_video_info(video_path)
    
    if info:
        print(f"Width: {info['width']}")
        print(f"Height: {info['height']}")
        print(f"Duration: {info['duration']} seconds")
        print(f"FPS: {info['fps']}")


def example_convert_video():
    """Example: Convert video to different format"""
    success = ffmpeg_service.convert_video(
        input_path="/path/to/input.mov",
        output_path="/path/to/output.mp4",
        format="mp4",
        resolution="1080p"
    )
    
    if success:
        print("✅ Video converted successfully!")


def example_apply_effects():
    """Example: Apply video effects"""
    effects = [
        "boxblur=5",  # Blur
        "unsharp=5:5:1.0",  # Sharpen
        "eq=brightness=0.1",  # Brightness
    ]
    
    success = ffmpeg_service.apply_effects(
        input_path="/path/to/video.mp4",
        output_path="/path/to/video_effects.mp4",
        effects=effects
    )
    
    if success:
        print("✅ Effects applied!")


def example_cut_video():
    """Example: Cut video segment"""
    success = ffmpeg_service.cut_video(
        input_path="/path/to/video.mp4",
        output_path="/path/to/clip.mp4",
        start_time="00:00:05",  # 5 seconds
        duration="00:00:30"  # 30 seconds
    )
    
    if success:
        print("✅ Video cut successfully!")


# ============ DATABASE EXAMPLES ============

from backend.config.database import SessionLocal
from backend.models.models import Video, Project, Clip

def example_create_project():
    """Example: Create a new project"""
    db = SessionLocal()
    
    project = Project(
        name="My Cool Video",
        description="A short promotional video",
        status="draft"
    )
    
    db.add(project)
    db.commit()
    db.refresh(project)
    
    print(f"✅ Project created with ID: {project.id}")
    db.close()


def example_query_videos():
    """Example: Query videos from database"""
    db = SessionLocal()
    
    # Get all videos
    videos = db.query(Video).all()
    
    for video in videos:
        print(f"- {video.title} ({video.duration}s)")
    
    # Filter by project
    project_videos = db.query(Video).filter(Video.project_id == 1).all()
    print(f"Videos in project 1: {len(project_videos)}")
    
    db.close()


def example_add_clip():
    """Example: Add clip to project"""
    db = SessionLocal()
    
    clip = Clip(
        project_id=1,
        source_video_id=1,
        title="Intro",
        start_time=0,  # milliseconds
        end_time=5000,  # 5 seconds
        track_index=0,
        order_index=0
    )
    
    db.add(clip)
    db.commit()
    
    print(f"✅ Clip created with ID: {clip.id}")
    db.close()


# ============ API EXAMPLES ============

import requests

BASE_URL = "http://localhost:8000/api"

def example_api_health_check():
    """Example: Health check API"""
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        print("✅ API is healthy!")
    else:
        print("❌ API is down!")


def example_api_download_video():
    """Example: Start download via API"""
    payload = {
        "url": "https://www.instagram.com/p/ABC123XYZ/",
    }
    
    response = requests.post(f"{BASE_URL}/downloads/start", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Download started with ID: {data['download_id']}")
        print(f"Progress: {data['progress']}%")


def example_api_get_projects():
    """Example: Get all projects via API"""
    response = requests.get(f"{BASE_URL}/projects")
    
    if response.status_code == 200:
        projects = response.json()
        
        for project in projects:
            print(f"- {project['name']} ({project['status']})")
            print(f"  Videos: {project['video_count']}")


def example_api_export_video():
    """Example: Export video via API"""
    payload = {
        "project_id": 1,
        "format": "mp4",
        "resolution": "1080p"
    }
    
    response = requests.post(f"{BASE_URL}/exports/start", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Export started with ID: {data['export_id']}")


# ============ FRONTEND EXAMPLES ============

from PyQt6.QtWidgets import QMessageBox
from frontend.main import MainWindow

def example_show_notification():
    """Example: Show notification in PyQt"""
    window = MainWindow()
    
    QMessageBox.information(
        window,
        "Success",
        "Video downloaded successfully!"
    )


def example_update_progress_bar():
    """Example: Update progress bar"""
    from PyQt6.QtWidgets import QProgressBar
    
    progress_bar = QProgressBar()
    progress_bar.setMaximum(100)
    
    for i in range(101):
        progress_bar.setValue(i)


# ============ VALIDATORS EXAMPLES ============

from backend.utils.validators import URLValidator, FileValidator

def example_validate_urls():
    """Example: Validate Instagram URLs"""
    urls = [
        "https://www.instagram.com/p/ABC123XYZ/",
        "https://www.instagram.com/reel/DEF456UVW/",
        "invalid-url",
    ]
    
    for url in urls:
        is_valid, message = URLValidator.validate_instagram_url(url)
        print(f"{url}: {message}")


def example_validate_files():
    """Example: Validate files"""
    is_valid, message = FileValidator.validate_video_file("video.mp4")
    print(f"Validation: {message}")


# ============ RUN EXAMPLES ============

if __name__ == "__main__":
    print("=== InstaVideo Studio API Examples ===\n")
    
    # Sync examples
    print("1. Video Info:")
    example_get_video_info()
    
    print("\n2. Database Query:")
    example_query_videos()
    
    print("\n3. API Health Check:")
    example_api_health_check()
    
    print("\n4. URL Validation:")
    example_validate_urls()
    
    # Async examples (run in event loop)
    print("\n5. Async Downloads:")
    asyncio.run(example_single_download())
