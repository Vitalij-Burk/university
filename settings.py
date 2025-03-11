from envparse import Env


env = Env()


REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres6910@localhost:5436/university",
)

TEST_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres6910_test@localhost:5437/university_test",
)
