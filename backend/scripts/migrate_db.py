import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import Base

load_dotenv()

# Try to get DATABASE_URL first (for Docker), fallback to individual variables
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # Fallback for local development
    SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', '904496Vfrc')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'roomscheduler')}"


def migrate_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


    with engine.connect() as conn:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        
        # Check if days table exists and has data
        try:
            result = conn.execute(text("SELECT COUNT(*) FROM days"))
            count = result.scalar()
            print(f"Days table has {count} records")
        except Exception as e:
            print(f"Days table is empty or doesn't exist: {e}")


if __name__ == "__main__":
    migrate_database()
