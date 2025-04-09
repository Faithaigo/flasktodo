from db import db
from datetime import datetime
from sqlalchemy import Boolean, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Data Model for Tasks
class Todo(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="tasks")
    
    def to_dict(self):
        return {"id": self.id, "title": self.title, "desc": self.description, 
                "description": self.description, "created_at": self.created_at,
                 "due_date": self.due_date, "user.id": self.user_id, "status": self.status}

    def __repr__(self):
        return f"<Task {self.title}>"
