from pydantic import BaseModel
import models


class Comment(BaseModel):
    id: int
    body: str
    user_id: int
    post_id: int

    class Config:
        from_atributes = True