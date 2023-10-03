import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from app.core.logger import init_logging
from app.ecommerce.v1 import ecommerce_router

load_dotenv(".env")

app = FastAPI(title="E-Commerce Admin Dashboard APIs")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])
app.include_router(ecommerce_router)

init_logging()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
