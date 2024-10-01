from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..dependencies import get_db
from fastapi_cache.decorator import cache
from typing import List
from fastapi_cache import FastAPICache

router = APIRouter()


async def cache_clear():
    return await FastAPICache.clear()


@router.post("/orders", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    for item in order.items:
        product = crud.get_product(db, item.product_id)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, detail=f"Not enough stock for product {product.id}")
    cache_clear()
    return crud.create_order(db, order)


@router.get("/orders", response_model=List[schemas.Order])
@cache(expire=60)
async def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=schemas.Order)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@router.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(order_id: int, status: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    cache_clear()
    return crud.update_order_status(db, order_id, status)


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    crud.delete_order(db, order_id)
    cache_clear()
    return {"message": "Order deleted successfully"}
