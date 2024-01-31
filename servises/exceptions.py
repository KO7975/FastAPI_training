from fastapi import HTTPException, status


user_not_exists = HTTPException(status_code=404, detail="User not exists")

user_already_exists = HTTPException(status_code=400, detail="User already exists")

wrong_password = HTTPException(status_code=400, detail="Wrong password")

wrong_credantials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

user_details_already_exists = HTTPException(status_code=400, detail="User details already exists")

user_details_not_exists = HTTPException(status_code=400, detail="User details not exists")
