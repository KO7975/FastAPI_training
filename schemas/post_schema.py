from pydantic import BaseModel
import models


class Post(BaseModel):
    id: int
    title: str
    text: str
    author_id: int
