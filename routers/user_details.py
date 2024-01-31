from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from routers.user import get_current_user
import models
from schemas.user_detail_schema import UserDetailBase, UserDetailInDB, UserDetail
from servises.account.user_details import (
    create_user_detail,
    get_user_detail,
    delete_user_detail,
    update_user_detail
)
from servises.exceptions import (
    user_details_already_exists,
    user_details_not_exists
)


router = APIRouter()


"""create user details"""
@router.post('/create_details/', tags=['User details'], response_model=UserDetailInDB)
async def create_user_details(
    details: UserDetailBase,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> models.UserDetail:
    detail = get_user_detail(db, current_user)
    if detail is None:
        return create_user_detail(db, details, current_user)
    raise user_details_already_exists


"""get user details"""
@router.get('/get_details/', tags=['User details'], response_model=UserDetailInDB)
async def get_user_details(
    db:Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
) -> models.UserDetail:
    
    details =  get_user_detail(db, user)
    if not details:
        raise user_details_not_exists
    return details


"""update user details"""
@router.patch('/update_details/', tags=['User details'], response_model=UserDetail)
async def update_details(
    details: UserDetailBase,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
) -> UserDetail: 
    return update_user_detail(db, user, details)
    
    
"""delete usr details"""
@router.delete('/delete_details/', tags=['User details'])
async def delete_details(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
) -> UserDetail:
    return delete_user_detail(db, user)
