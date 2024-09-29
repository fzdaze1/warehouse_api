from fastapi import FastAPI
from .api import products, orders


app = FastAPI()


app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
