from fastapi import APIRouter

from app.ecommerce.v1.views import router

API_PREFIX = "/api/v1"

ecommerce_router = APIRouter(prefix=API_PREFIX)
ecommerce_router.include_router(router)
