from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:SecondeDatabaseDB@db.tltrkvhxvwysuhbfkdyp.pooler.supabase.co:6543/postgres"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # important pour cloud
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
