from sqlalchemy.orm import Session
import models
from schemas.user_schema import User, UserInDB
from schemas.user_detail_schema import UserDetailCreate, UserDetail


def create_user_detail(
        db:Session,
        details: UserDetailCreate,
        user: User
) -> models.UserDetail:
    if details is not None:
        detail = models.UserDetail(**details.model_dump())
        detail.user_id = user.id
        db.add(detail)
        db.commit()  
        db.refresh(detail)
        return detail
    return {}


def get_user_detail(db: Session, user: User) -> models.UserDetail:
    return db.query(models.UserDetail).filter(models.UserDetail.user_id==user.id).first()


def delete_user_detail(db: Session, user: User):
    detail = db.query(models.UserDetail).filter(models.UserDetail.user_id == user.id)
    detail.delete()
    db.commit()
    return detail


def update_user_detail(
        db: Session,
        user: User,
        details: UserDetail
) -> models.UserDetail:
    detail = db.query(models.UserDetail).filter(models.UserDetail.user_id == user.id).first()
    detail.phone = details.phone
    detail.adress = details.adress
    db.commit()
    db.refresh(detail)
    return detail


def remove_details(user: User) -> models.User:
    data = user.__dict__.copy()
    details = {}
    if user.details:
        details = user.details[0].__dict__.copy()

    user_in_db = UserInDB(**data, details=details)
    return user_in_db