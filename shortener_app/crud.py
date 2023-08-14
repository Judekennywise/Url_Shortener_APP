from sqlalchemy.orm import Session

from keygen import *
from models import * 
from schemas import *

def create_db_url(db: Session, url: URLBase) -> URL:
    key = create_unique_random_key(db)
    secret_key = f"{key}_{create_random_key(length=8)}"
    db_url = URL(
        target_url=url.target_url, key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str) -> URL:
    return (
        db.query(URL)
        .filter(URL.key == url_key, URL.is_active)
        .first()
    )

def get_db_url_by_secret_key(db: Session, secret_key: str) -> URL:
    return (
        db.query(URL)
        .filter(URL.secret_key == secret_key, URL.is_active)
        .first()
    )

def update_db_clicks(db: Session, db_url: URL) -> URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> URL:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url