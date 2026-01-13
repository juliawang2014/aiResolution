#!/usr/bin/env python3
"""
Simple database connection test
"""

import sys
import os
import sqlite3
from pathlib import Path

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

def test_sqlite_direct():
    """Test SQLite connection directly"""
    print("🔧 Testing direct SQLite connection...")
    
    try:
        # Create database file if it doesn't exist
        db_path = os.path.join(project_root, "goals.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test basic operation
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        conn.close()
        print(f"✅ Direct SQLite connection successful: {result}")
        print(f"📁 Database file: {os.path.abspath(db_path)}")
        return True
        
    except Exception as e:
        print(f"❌ Direct SQLite connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    print("\n🔧 Testing SQLAlchemy connection...")
    
    try:
        from app.database import engine, SessionLocal
        from sqlalchemy import text
        
        # Test engine connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).fetchone()
            print(f"✅ SQLAlchemy engine connection successful: {result}")
        
        # Test session
        db = SessionLocal()
        try:
            result = db.execute(text("SELECT 1")).fetchone()
            print(f"✅ SQLAlchemy session connection successful: {result}")
        finally:
            db.close()
            
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_models():
    """Test model creation"""
    print("\n🔧 Testing model creation...")
    
    try:
        from app.database import engine
        from app import models
        
        # Create tables
        models.Base.metadata.create_all(bind=engine)
        print("✅ Models and tables created successfully")
        
        # List created tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"📋 Created tables: {tables}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🎯 Database Connection Test")
    print("=" * 50)
    
    # Test 1: Direct SQLite
    if not test_sqlite_direct():
        return
    
    # Test 2: SQLAlchemy connection
    if not test_sqlalchemy_connection():
        return
    
    # Test 3: Model creation
    if not test_models():
        return
    
    print("\n🎉 All database tests passed!")
    print("✅ Database is ready for the Goal Tracker application")

if __name__ == "__main__":
    main()