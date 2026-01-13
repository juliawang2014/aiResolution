#!/usr/bin/env python3
"""
Test script to verify database setup and goal creation
"""

import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from app.database import SessionLocal, engine
from app import models, schemas, crud

def test_database():
    print("🔧 Testing database setup...")
    
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Test database connection
    db = SessionLocal()
    try:
        # Test creating a simple goal
        test_goal = schemas.GoalCreate(
            title="Test Goal",
            description="This is a test goal",
            category="Test"
        )
        
        print("📝 Creating test goal...")
        db_goal = crud.create_goal(db=db, goal=test_goal)
        print(f"✅ Goal created with ID: {db_goal.id}")
        
        # Test retrieving goals
        goals = crud.get_goals(db)
        print(f"✅ Retrieved {len(goals)} goals from database")
        
        # Clean up test goal
        db.delete(db_goal)
        db.commit()
        print("🧹 Test goal cleaned up")
        
        print("🎉 Database test completed successfully!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_database()