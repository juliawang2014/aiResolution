#!/usr/bin/env python3
"""
Test only the delete functionality
"""

import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from app.database import SessionLocal
from app import models, schemas, crud

def test_delete_functionality():
    print("🗑️ Testing Delete Functionality")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Create a test goal first
        print("📝 Creating test goal...")
        test_goal = schemas.GoalCreate(
            title="Test Delete Goal",
            description="This goal will be deleted",
            category="Test"
        )
        
        db_goal = crud.create_goal(db=db, goal=test_goal)
        goal_id = db_goal.id
        print(f"✅ Created goal with ID: {goal_id}")
        
        # Add a progress entry
        print("📊 Adding progress entry...")
        progress_entry = schemas.ProgressEntryCreate(
            goal_id=goal_id,
            text="Test progress entry",
            progress_percentage=50.0,
            sentiment="positive"
        )
        
        db_progress = crud.create_progress_entry(db=db, progress=progress_entry)
        print(f"✅ Created progress entry with ID: {db_progress.id}")
        
        # Verify goal exists with progress
        goal_before = crud.get_goal(db, goal_id)
        progress_before = crud.get_progress_entries(db, goal_id)
        print(f"📋 Goal exists: {goal_before is not None}")
        print(f"📋 Progress entries: {len(progress_before)}")
        
        # Test deletion
        print("🗑️ Deleting goal...")
        success = crud.delete_goal(db=db, goal_id=goal_id)
        print(f"✅ Delete operation success: {success}")
        
        # Verify deletion
        goal_after = crud.get_goal(db, goal_id)
        progress_after = crud.get_progress_entries(db, goal_id)
        print(f"📋 Goal exists after deletion: {goal_after is not None}")
        print(f"📋 Progress entries after deletion: {len(progress_after)}")
        
        if goal_after is None and len(progress_after) == 0:
            print("🎉 Delete functionality works correctly!")
            return True
        else:
            print("❌ Delete functionality failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during delete test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_delete_functionality()