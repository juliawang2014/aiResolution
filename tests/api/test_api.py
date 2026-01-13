#!/usr/bin/env python3
"""
Test the Goal Tracker API endpoints
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("🔧 Testing Goal Tracker API...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: Get goals (should be empty initially)
    try:
        response = requests.get(f"{base_url}/goals")
        if response.status_code == 200:
            goals = response.json()
            print(f"✅ Get goals successful: {len(goals)} goals found")
        else:
            print(f"❌ Get goals failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get goals failed: {e}")
        return False
    
    # Test 3: Create a goal
    try:
        goal_data = {
            "title": "Test API Goal",
            "description": "This is a test goal created via API",
            "category": "Test"
        }
        
        response = requests.post(
            f"{base_url}/goals",
            headers={"Content-Type": "application/json"},
            data=json.dumps(goal_data)
        )
        
        if response.status_code == 200:
            created_goal = response.json()
            print(f"✅ Create goal successful: ID {created_goal['id']}")
            return created_goal
        else:
            print(f"❌ Create goal failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Create goal failed: {e}")
        return False

def test_delete_goal(goal_id):
    """Test deleting a goal"""
    base_url = "http://localhost:8000"
    
    try:
        response = requests.delete(f"{base_url}/goals/{goal_id}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Delete goal successful: {result['message']}")
            return True
        else:
            print(f"❌ Delete goal failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Delete goal failed: {e}")
        return False

def main():
    print("🎯 API Test Suite")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Test basic API functionality
    result = test_api()
    
    if result:
        print("\n🔄 Testing delete functionality...")
        
        # Test delete with the created goal
        goal_id = result['id']
        delete_result = test_delete_goal(goal_id)
        
        if delete_result:
            print("\n🎉 All API tests passed!")
            print("✅ The Goal Tracker API is working correctly")
            print("🌐 You can now test the frontend at http://localhost:3000")
            print("🗑️ Delete functionality is now available!")
        else:
            print("\n❌ Delete tests failed")
    else:
        print("\n❌ API tests failed")
        print("🔍 Check if the server is running: python debug_start.py")

if __name__ == "__main__":
    main()

