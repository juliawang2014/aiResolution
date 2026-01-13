from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import json
from typing import List
import asyncio
from datetime import datetime

from . import models, schemas, crud
from .database import SessionLocal, engine
from .nlp_processor import NLPProcessor
from .websocket_manager import ConnectionManager

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Goal Tracker API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
manager = ConnectionManager()
nlp_processor = NLPProcessor()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/")
async def root():
    return {"message": "Goal Tracker API is running"}

@app.post("/goals", response_model=schemas.Goal)
async def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    """Create a new goal"""
    db_goal = crud.create_goal(db=db, goal=goal)
    
    # Broadcast to all connected clients
    await manager.broadcast({
        "type": "goal_created",
        "data": schemas.Goal.from_orm(db_goal).dict()
    })
    
    return db_goal

@app.get("/goals", response_model=List[schemas.Goal])
async def list_goals(db: Session = Depends(get_db)):
    """List all goals"""
    return crud.get_goals(db)

@app.get("/goals/{goal_id}", response_model=schemas.Goal)
async def get_goal(goal_id: int, db: Session = Depends(get_db)):
    """Get a specific goal"""
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

@app.post("/goals/{goal_id}/update")
async def update_goal_progress(
    goal_id: int, 
    update: schemas.ProgressUpdate, 
    db: Session = Depends(get_db)
):
    """Add a progress update using natural language"""
    # Get the goal
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Process the natural language update
    analysis = nlp_processor.analyze_progress_update(update.text, db_goal.title)
    
    # Create progress entry
    progress_data = schemas.ProgressEntryCreate(
        goal_id=goal_id,
        text=update.text,
        progress_percentage=analysis.get("progress_percentage", 0),
        sentiment=analysis.get("sentiment", "neutral"),
        key_insights=analysis.get("insights", [])
    )
    
    db_progress = crud.create_progress_entry(db=db, progress=progress_data)
    
    # Update goal progress
    crud.update_goal_progress(db=db, goal_id=goal_id, progress=analysis.get("progress_percentage", 0))
    
    # Generate AI feedback
    feedback = nlp_processor.generate_feedback(db_goal, analysis)
    
    # Broadcast update
    await manager.broadcast({
        "type": "progress_updated",
        "data": {
            "goal_id": goal_id,
            "progress": schemas.ProgressEntry.from_orm(db_progress).dict(),
            "feedback": feedback,
            "updated_goal": schemas.Goal.from_orm(crud.get_goal(db, goal_id)).dict()
        }
    })
    
    return {
        "progress": db_progress,
        "feedback": feedback,
        "analysis": analysis
    }

@app.get("/dashboard")
async def get_dashboard_data(db: Session = Depends(get_db)):
    """Get public dashboard data"""
    goals = crud.get_goals(db)
    stats = crud.get_goal_statistics(db)
    
    return {
        "goals": [schemas.Goal.from_orm(goal).dict() for goal in goals],
        "statistics": stats,
        "last_updated": "now"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle any client messages if needed
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)