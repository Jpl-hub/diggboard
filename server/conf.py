from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

uri = 'mysql+pymysql://root:abc123@localhost/dashboard'

engine = create_engine(uri)
session = sessionmaker(bind=engine)

async_uri = 'mysql+aiomysql://root:abc123@localhost/dashboard'
async_engine = create_async_engine(async_uri)
asyncSession = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
