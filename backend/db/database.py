from sqlalchemy.ext.asyncio import create_async_engine
import settings
import databases

# DB Credentials
db_username = settings.DB_USER
db_db = settings.DB_DB
db_host = settings.DB_HOST
db_port = settings.DB_PORT
db_password = settings.DB_PASSWORD

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_password}@{db_host}:{db_port}/{db_db}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=20)

database = databases.Database(SQLALCHEMY_DATABASE_URL)
