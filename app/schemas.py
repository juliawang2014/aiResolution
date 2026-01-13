from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    goal_id: int
    created_at: datetime

class Goal(GoalBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    progress_percentage: float
    status: str
    progress_entries: List[ProgressEntry] = []

class ProgressUpdate(BaseModel):
    text: str

class DashboardStats(BaseModel):
    total_goals: int
    completed_goals: int
    active_goals: int
    average_progress: float
    goals_by_category: dict

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    target_date: Optional[datetime] = None
    status: Optional[str] = None