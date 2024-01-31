from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from settings import ACCESS_TOKEN_EXPIRE_HOURS
from database import get_db
from schemas.auth_schema import Token
from schemas.user_schema import (
    User,
    UserCreate,
    UserInDB,
)
from servises.account.user_data import (
    get_user,
    user_get_by_email,
    get_password_hash,
    create_user,
    update_email,
    update_password,
    user_delete,
)
from servises.account.authorization import (
    oauth2_scheme,
    get_by_username,
    get_current,
    create_access_token,
    authenticate_user,
)
from servises.exceptions import (
    user_not_exists,
    user_already_exists,
    wrong_password,
    wrong_credantials
)
from servises.account.user_details import get_user_detail, remove_details


router = APIRouter()


# """Get authorized user data"""
@router.get("/me/", tags=['user'], response_model=UserInDB)
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> UserInDB:
    
    current_user = get_current(db, token)

    return remove_details(current_user)


"""Get user by id"""
@router.get('/{id}/', tags=["user"], response_model=UserInDB)
async def get_user_by_id(
    id: int = None,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserInDB:
    
    user = get_user(db=db, user_id=id)
    if user is None:
        raise user_not_exists
    
    return remove_details(user)


"""Get user by email"""
@router.post('/{email}/', tags=["user"], response_model=UserInDB)
async def get_user_by_email(
    email: str = None,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    
    user = user_get_by_email(db=db, email=email)

    if user is None:
        raise user_not_exists
    
    return remove_details(user)


"""Get user by username"""
@router.post('/{username}/', tags=["user"], response_model=UserInDB)
async def get_user_by_username(
    username: str = None,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    
    user = get_by_username(db=db, username=username)

    if user is None:
        raise user_not_exists
    
    return remove_details(user)


"""Create new user"""
@router.post("/", tags=["user"])
async def create_new_user(
    user:UserCreate,
    db:Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
) -> User:
    
    db_user = user_get_by_email(db=db, email=user.email)

    if db_user:
        raise user_already_exists
    
    return create_user(db=db, user=user)


"""Update user pasword"""
@router.put('/{id}/', tags=["user"])
async def user_update_password(
    id: int ,
    present_password: str,
    new_password: str,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    
    user = get_user(db=db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not exists")

    elif user.password == get_password_hash(present_password):
        return update_password(db=db, user_id=id, password=new_password)
    
    return wrong_password


"""Update user email"""
@router.patch('/{id}/', tags=['user'])
async def user_update_email(
    id: int,
    password: str, 
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    
    user = get_user(db=db, user_id=id)
    if user is None:
        raise user_not_exists

    elif user.password == password:
        return update_email(db=db, user_id=id, email=email)
    return wrong_password


"""Delete user"""
@router.delete('/{id}/', tags=['user'])
async def delete_user(
    id: int,
    password: str,
    db: Session= Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> User:
    
    user = get_user(db=db, user_id=id)

    if user and user.password == password:
        return user_delete(db=db, user_id=id)
        
    return user_not_exists


"""Get token"""
@router.post("/token", response_model=Token)
async def login_for_access_token( 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise wrong_credantials

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
