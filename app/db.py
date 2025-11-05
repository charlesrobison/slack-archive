from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create SQLAlchemy engine with connection pooling
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)
