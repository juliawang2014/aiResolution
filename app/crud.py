from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import List

def get_goal(db: Session, goal_id: int):
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()

def get_goals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Goal).offset(skip).limit(limit).all()

def create_goal(db: Session, goal: schemas.GoalCreate):
    db_goal = models.Goal(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal_progress(db: Session, goal_id: int, progress: float):
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if db_goal:
        db_goal.progress_percentage = min(100.0, max(0.0, progress))
        if db_goal.progress_percentage >= 100.0:
            db_goal.status = "completed"
        db.commit()
        db.refresh(db_goal)
    return db_goal

def create_progress_entry(db: Session, progress: schemas.ProgressEntryCreate):
    db_progress = models.ProgressEntry(**progress.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

def get_progress_entries(db: Session, goal_id: int):
    return db.query(models.ProgressEntry).filter(
        models.ProgressEntry.goal_id == goal_id
    ).order_by(models.ProgressEntry.created_at.desc()).all()

def get_goal_statistics(db: Session):
    total_goals = db.query(models.Goal).count()
    completed_goals = db.query(models.Goal).filter(models.Goal.status == "completed").count()
    active_goals = db.query(models.Goal).filter(models.Goal.status == "active").count()
    
    avg_progress = db.query(func.avg(models.Goal.progress_percentage)).scalar() or 0.0
    
    # Goals by category
    category_stats = db.query(
        models.Goal.category, 
        func.count(models.Goal.id)
    ).group_by(models.Goal.category).all()
    
    goals_by_category = {category or "Uncategorized": count for category, count in category_stats}
    
    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "active_goals": active_goals,
        "average_progress": round(avg_progress, 2),
        "goals_by_category": goals_by_category
    }