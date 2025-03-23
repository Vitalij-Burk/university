from random import randint

from fastapi import APIRouter


service_router = APIRouter()


@service_router.get("/ping")
async def ping():
    if randint(1, 10) % 2 == 0:
        raise ValueError
    raise ZeroDivisionError
    return {"Success": True}
