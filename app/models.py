from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    category = Column(String, index=True)
    target_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    progress_percentage = Column(Float, default=0.0)
    status = Column(String, default="active")  # active, completed, paused, cancelled
    
    # Relationships
    progress_entries = relationship("ProgressEntry", back_populates="goal", order_by="ProgressEntry.created_at.desc()")

class ProgressEntry(Base):
    __tablename__ = "progress_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"))
    text = Column(Text, nullable=False)
    progress_percentage = Column(Float)
    sentiment = Column(String)  # positive, negative, neutral
    key_insights = Column(JSON)  # List of extracted insights
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    goal = relationship("Goal", back_populates="progress_entries")