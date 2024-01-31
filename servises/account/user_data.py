from sqlalchemy.orm import Session
from models import User
from schemas.user_schema import UserCreate
from servises.account.authorization import get_password_hash


def create_user(db:Session, user:UserCreate) -> User:
    db_user = User(**user.model_dump())
    db_user.password = get_password_hash(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db:Session, user_id:int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def user_get_by_email(db:Session, email:str) -> User:
    return db.query(User).filter(User.email == email).first()

        
def update_password(db:Session, user_id:int, password:str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    user.password = get_password_hash(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_email(db:Session, user_id:int, email:str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    user.email = email
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_delete(db:Session, user_id:int) -> User:
    db_user = db.query(User).filter(User.id == user_id)
    db_user.delete()
    db.commit()
    return db_user
