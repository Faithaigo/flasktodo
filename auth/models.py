from db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from flask_login import UserMixin


# Data Model for Users
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}
    
    def __repr__(self):
        return f"<User {self.username}>"