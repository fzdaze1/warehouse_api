from sqlalchemy.orm import Session
from . import models, schemas


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(status="в процессе")
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for item in order.items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_order_item)

        product = db.query(models.Product).filter(
            models.Product.id == item.product_id).first()
        product.stock -= item.quantity

    db.commit()
    return db_order


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order_status(db: Session, order_id: int, status: schemas.OrderStatusUpdate):
    db_order = db.query(models.Order).filter(
        models.Order.id == order_id).first()
    db_order.status = status.status
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(
        models.Order.id == order_id).first()
    db.delete(db_order)
    db.commit()
