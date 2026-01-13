#!/usr/bin/env python3
"""
Debug startup script for Goal Tracker
This script will help identify and fix the goal creation issue
"""

import uvicorn
import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from app.database import SessionLocal, engine
from app import models

def setup_database():
    """Initialize the database"""
    print("🔧 Setting up database...")
    
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    # Test database connection
    db = SessionLocal()
    try:
        from sqlalchemy import text
        # Simple query to test connection
        result = db.execute(text("SELECT 1")).fetchone()
        print("✅ Database connection test successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        db.close()
    
    return True

def main():
    print("🎯 Goal Tracker Debug Startup")
    print("=" * 50)
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed. Exiting.")
        return
    
    print("\n🚀 Starting FastAPI server with debug logging...")
    print("📊 Dashboard will be available at: http://localhost:3000")
    print("🔌 API will be available at: http://localhost:8000")
    print("📋 API docs will be available at: http://localhost:8000/docs")
    print("\n" + "=" * 50)
    
    # Start the server with debug logging
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )

if __name__ == "__main__":
    main()