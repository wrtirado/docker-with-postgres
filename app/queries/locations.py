from app.models.pydantic import locations
from sqlalchemy.orm import Session
from app.models.sqlalchemy import locations


def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(locations.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: locations.ItemCreate):
    db_item = locations.Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: locations.ItemCreate):
    db_item = db.query(locations.Item).filter(locations.Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(locations.Item).filter(locations.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
