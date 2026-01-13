from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    target_date: Optional[datetime] = None

class GoalCreate(GoalBase):
    pass

class ProgressEntryBase(BaseModel):
    text: str
    progress_percentage: Optional[float] = None
    sentiment: Optional[str] = None
    key_insights: Optional[List[str]] = None

class ProgressEntryCreate(ProgressEntryBase):
    goal_id: int

class ProgressEntry(ProgressEntryBase):
    id: int
    goal_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Goal(GoalBase):
    id: int
    created_at: datetime
    updated_at: datetime
    progress_percentage: float
    status: str
    progress_entries: List[ProgressEntry] = []
    
    class Config:
        from_attributes = True

class ProgressUpdate(BaseModel):
    text: str

class DashboardStats(BaseModel):
    total_goals: int
    completed_goals: int
    active_goals: int
    average_progress: float
    goals_by_category: dict