"""
Video Model
SQLAlchemy ORM model for Videos
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from config.database import Base


class Video(Base):
    """Video model representing downloaded or imported videos"""
    
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    url_source = Column(String(500), unique=True, index=True)
    thumbnail_path = Column(String(500))
    file_path = Column(String(500), nullable=False)
    duration = Column(Integer)  # seconds
    resolution = Column(String(50))  # e.g., "1920x1080"
    file_size = Column(Integer)  # bytes
    
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"))
    
    author = Column(String(255))
    tags = Column(Text)  # JSON array as string
    metadata = Column(Text)  # JSON metadata
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="videos")
    clips = relationship("Clip", back_populates="source_video", cascade="all, delete-orphan")
    in_queue = relationship("DownloadQueue", back_populates="video")
    
    def __repr__(self) -> str:
        return f"<Video(id={self.id}, title='{self.title}', duration={self.duration}s)>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url_source": self.url_source,
            "thumbnail_path": self.thumbnail_path,
            "file_path": self.file_path,
            "duration": self.duration,
            "resolution": self.resolution,
            "file_size": self.file_size,
            "project_id": self.project_id,
            "author": self.author,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Project(Base):
    """Project model for managing video editing projects"""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    thumbnail_path = Column(String(500))
    status = Column(String(50), default="draft")  # draft, processing, completed, archived
    
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    videos = relationship("Video", back_populates="project", cascade="all, delete-orphan")
    clips = relationship("Clip", back_populates="project", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="project", cascade="all, delete-orphan")
    text_overlays = relationship("TextOverlay", back_populates="project", cascade="all, delete-orphan")
    audio_tracks = relationship("AudioTrack", back_populates="project", cascade="all, delete-orphan")
    scheduled_posts = relationship("ScheduledPost", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "thumbnail_path": self.thumbnail_path,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "modified_at": self.modified_at.isoformat() if self.modified_at else None,
            "video_count": len(self.videos),
            "clip_count": len(self.clips),
        }


class Clip(Base):
    """Clip model for video segments in projects"""
    
    __tablename__ = "clips"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    source_video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255))
    start_time = Column(Integer, nullable=False)  # milliseconds
    end_time = Column(Integer, nullable=False)  # milliseconds
    duration = Column(Integer)  # milliseconds
    track_index = Column(Integer, default=0)
    order_index = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="clips")
    source_video = relationship("Video", back_populates="clips")
    effects = relationship("Effect", back_populates="clip", cascade="all, delete-orphan")
    text_overlays = relationship("TextOverlay", back_populates="clip")
    from_transitions = relationship("Transition", foreign_keys="Transition.from_clip_id", cascade="all, delete-orphan")
    to_transitions = relationship("Transition", foreign_keys="Transition.to_clip_id")
    
    def __repr__(self) -> str:
        return f"<Clip(id={self.id}, duration={self.duration}ms, track={self.track_index})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "source_video_id": self.source_video_id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "track_index": self.track_index,
            "order_index": self.order_index,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Export(Base):
    """Export model for tracking video exports"""
    
    __tablename__ = "exports"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    format = Column(String(50), nullable=False)  # mp4, mov, avi, mkv
    resolution = Column(String(50), nullable=False)  # 720p, 1080p, 1440p, 4k
    file_path = Column(String(500))
    file_size = Column(Integer)  # bytes
    
    status = Column(String(50), default="pending")  # pending, processing, completed, failed, cancelled
    progress = Column(Integer, default=0)  # 0-100
    
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="exports")
    
    def __repr__(self) -> str:
        return f"<Export(id={self.id}, format='{self.format}', resolution='{self.resolution}', status='{self.status}')>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "format": self.format,
            "resolution": self.resolution,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "status": self.status,
            "progress": self.progress,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Effect(Base):
    """Effect model for video effects"""
    
    __tablename__ = "effects"
    
    id = Column(Integer, primary_key=True, index=True)
    clip_id = Column(Integer, ForeignKey("clips.id", ondelete="CASCADE"), nullable=False)
    effect_type = Column(String(50), nullable=False)
    effect_name = Column(String(255))
    parameters = Column(Text)  # JSON
    start_time = Column(Integer)  # milliseconds
    end_time = Column(Integer)  # milliseconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    clip = relationship("Clip", back_populates="effects")
    
    def __repr__(self) -> str:
        return f"<Effect(id={self.id}, type='{self.effect_type}')>"


class TextOverlay(Base):
    """Text/Subtitle overlay model"""
    
    __tablename__ = "text_overlays"
    
    id = Column(Integer, primary_key=True, index=True)
    clip_id = Column(Integer, ForeignKey("clips.id", ondelete="SET NULL"))
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    content = Column(Text, nullable=False)
    font_family = Column(String(50), default="Arial")
    font_size = Column(Integer, default=24)
    font_color = Column(String(7), default="#FFFFFF")
    background_color = Column(String(7))
    
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    width = Column(Integer)
    height = Column(Integer)
    opacity = Column(Integer, default=100)  # 0-100
    
    start_time = Column(Integer, nullable=False)  # milliseconds
    end_time = Column(Integer, nullable=False)  # milliseconds
    animation = Column(Text)  # JSON
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    clip = relationship("Clip", back_populates="text_overlays")
    project = relationship("Project", back_populates="text_overlays")
    
    def __repr__(self) -> str:
        return f"<TextOverlay(id={self.id}, content='{self.content[:20]}...')>"


class AudioTrack(Base):
    """Audio track model"""
    
    __tablename__ = "audio_tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(500))
    title = Column(String(255))
    duration = Column(Integer)  # milliseconds
    volume = Column(Integer, default=100)  # 0-100
    start_time = Column(Integer, default=0)  # milliseconds
    is_music = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="audio_tracks")
    
    def __repr__(self) -> str:
        return f"<AudioTrack(id={self.id}, title='{self.title}')>"


class Transition(Base):
    """Transition effect between clips"""
    
    __tablename__ = "transitions"
    
    id = Column(Integer, primary_key=True, index=True)
    from_clip_id = Column(Integer, ForeignKey("clips.id", ondelete="CASCADE"), nullable=False)
    to_clip_id = Column(Integer, ForeignKey("clips.id", ondelete="CASCADE"), nullable=False)
    transition_type = Column(String(50), nullable=False)
    duration = Column(Integer, default=500)  # milliseconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Transition(id={self.id}, type='{self.transition_type}')>"


class DownloadQueue(Base):
    """Download queue item"""
    
    __tablename__ = "download_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    status = Column(String(50), default="pending")
    progress = Column(Integer, default=0)
    file_size = Column(Integer)
    downloaded_size = Column(Integer, default=0)
    video_id = Column(Integer, ForeignKey("videos.id", ondelete="SET NULL"))
    
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    video = relationship("Video", back_populates="in_queue")
    
    def __repr__(self) -> str:
        return f"<DownloadQueue(id={self.id}, status='{self.status}', progress={self.progress}%)>"


class InstagramAccount(Base):
    """Instagram connected account"""
    
    __tablename__ = "instagram_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    access_token = Column(String(500), nullable=False)
    refresh_token = Column(String(500))
    expires_at = Column(DateTime)
    connected = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    scheduled_posts = relationship("ScheduledPost", back_populates="instagram_account")
    
    def __repr__(self) -> str:
        return f"<InstagramAccount(id={self.id}, username='{self.username}')>"


class ScheduledPost(Base):
    """Scheduled Instagram post"""
    
    __tablename__ = "scheduled_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    instagram_account_id = Column(Integer, ForeignKey("instagram_accounts.id", ondelete="CASCADE"), nullable=False)
    
    caption = Column(Text)
    scheduled_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="scheduled")  # scheduled, published, failed, cancelled
    posted_at = Column(DateTime)
    error_message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="scheduled_posts")
    instagram_account = relationship("InstagramAccount", back_populates="scheduled_posts")
    
    def __repr__(self) -> str:
        return f"<ScheduledPost(id={self.id}, status='{self.status}')>"


class Setting(Base):
    """Application settings"""
    
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, nullable=False)
    value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Setting(key='{self.key}', value='{self.value}')>"
