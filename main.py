import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette_exporter import handle_metrics
from starlette_exporter import PrometheusMiddleware

import settings
from api.handlers import user_router
from api.login_handlers import login_router
from api.service import service_router


sentry_sdk.init("https://055a6010a95e4051b617f1463c38190e@app.glitchtip.com/10720")

app = FastAPI(title="university")

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["User"])
main_api_router.include_router(login_router, prefix="/login", tags=["Login"])
main_api_router.include_router(service_router, prefix="/service", tags=["Service"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
