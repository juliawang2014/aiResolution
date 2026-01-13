#!/usr/bin/env python3
"""
Sample data generator for Goal Tracker
Run this script to populate the database with example goals and progress entries.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from app.database import SessionLocal
from app import models, schemas, crud

def create_sample_data():
    db = SessionLocal()
    
    try:
        # Sample goals
        sample_goals = [
            {
                "title": "Learn Spanish Fluently",
                "description": "Achieve conversational fluency in Spanish by practicing daily and completing an online course.",
                "category": "Education",
                "target_date": datetime.now() + timedelta(days=365),
                "progress": 25
            },
            {
                "title": "Run a Half Marathon",
                "description": "Train consistently to complete a 21K run in under 2 hours.",
                "category": "Health & Fitness", 
                "target_date": datetime.now() + timedelta(days=180),
                "progress": 45
            },
            {
                "title": "Launch My Side Project",
                "description": "Build and deploy a web application that solves a real problem for users.",
                "category": "Career",
                "target_date": datetime.now() + timedelta(days=120),
                "progress": 60
            },
            {
                "title": "Read 24 Books This Year",
                "description": "Read at least 2 books per month across different genres to expand knowledge.",
                "category": "Personal",
                "target_date": datetime.now() + timedelta(days=300),
                "progress": 33
            },
            {
                "title": "Save $10,000 Emergency Fund",
                "description": "Build a solid emergency fund by saving consistently each month.",
                "category": "Financial",
                "target_date": datetime.now() + timedelta(days=240),
                "progress": 70
            }
        ]
        
        created_goals = []
        
        for goal_data in sample_goals:
            # Create goal
            goal_create = schemas.GoalCreate(
                title=goal_data["title"],
                description=goal_data["description"],
                category=goal_data["category"],
                target_date=goal_data["target_date"]
            )
            
            db_goal = crud.create_goal(db=db, goal=goal_create)
            crud.update_goal_progress(db=db, goal_id=db_goal.id, progress=goal_data["progress"])
            created_goals.append(db_goal)
            
            print(f"✅ Created goal: {goal_data['title']}")
        
        # Add sample progress entries
        sample_updates = [
            {
                "goal_id": created_goals[0].id,  # Spanish
                "text": "Completed lesson 5 today! Learning about past tense verbs. Feeling confident about my progress so far.",
                "days_ago": 2
            },
            {
                "goal_id": created_goals[1].id,  # Half Marathon
                "text": "Ran 8km today in 45 minutes. My endurance is definitely improving week by week!",
                "days_ago": 1
            },
            {
                "goal_id": created_goals[2].id,  # Side Project
                "text": "Finished the user authentication system. About 60% done with the core features now.",
                "days_ago": 3
            },
            {
                "goal_id": created_goals[3].id,  # Reading
                "text": "Just finished 'Atomic Habits' - amazing book! That's 8 books down, 16 to go.",
                "days_ago": 5
            },
            {
                "goal_id": created_goals[4].id,  # Emergency Fund
                "text": "Saved another $500 this month. I'm at $7,000 now - so close to my goal!",
                "days_ago": 7
            }
        ]
        
        for update in sample_updates:
            # Create progress entry with backdated timestamp
            created_at = datetime.now() - timedelta(days=update["days_ago"])
            
            progress_entry = models.ProgressEntry(
                goal_id=update["goal_id"],
                text=update["text"],
                progress_percentage=None,  # Will be analyzed by NLP
                sentiment="positive",
                key_insights=["Making steady progress"],
                created_at=created_at
            )
            
            db.add(progress_entry)
            
        db.commit()
        print(f"✅ Added {len(sample_updates)} progress updates")
        
        print("\n🎯 Sample data created successfully!")
        print("You can now start the application and see the sample goals in action.")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()