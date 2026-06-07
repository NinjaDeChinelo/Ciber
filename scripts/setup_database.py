"""
Setup database script
Initialize SQLite database with schema
"""

import sqlite3
import sys
from pathlib import Path
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from database.schema import CREATE_TABLES_SQL


def setup_database(force: bool = False) -> bool:
    """
    Initialize database with schema
    
    Args:
        force: Force recreation of database
    """
    try:
        db_file = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
        
        # Remove existing database if force flag
        if force and db_file.exists():
            logger.warning(f"Removing existing database: {db_file}")
            db_file.unlink()
        
        # Create database file
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Connect and execute schema
        connection = sqlite3.connect(str(db_file))
        cursor = connection.cursor()
        
        logger.info(f"Creating database schema at {db_file}...")
        
        # Execute all CREATE TABLE statements
        for statement in CREATE_TABLES_SQL.split(";"):
            statement = statement.strip()
            if statement:
                cursor.execute(statement)
        
        connection.commit()
        connection.close()
        
        logger.info("✅ Database initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False


if __name__ == "__main__":
    force = "--force" in sys.argv
    
    if not setup_database(force):
        sys.exit(1)
    
    logger.info("Setup completed!")
