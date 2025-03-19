from envparse import Env


env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres6910@localhost:5436/university",
)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres6910_test@localhost:5437/university_test",
)

APP_PORT = env.int("APP_PORT", default=8000)
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
