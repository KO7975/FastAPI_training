from sqlalchemy import Column, String, Integer, TIMESTAMP, text, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    role = Column(String, index=True)

    details = relationship("UserDetail", back_populates='user')


class UserDetail(Base):
    __tablename__ = "details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    adress = Column(String)
    phone = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    user = relationship("User", back_populates="details")


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    