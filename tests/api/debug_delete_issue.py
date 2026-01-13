#!/usr/bin/env python3
"""
Debug script to identify the specific delete issue
"""

import requests
import json
import sys
import os

def debug_delete_issue():
    print("🔍 Debugging Goal Delete Issue")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Step 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Server is running: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return
    
    # Step 2: Create a test goal
    print("\n📝 Creating test goal...")
    try:
        goal_data = {
            "title": "Debug Delete Goal",
            "description": "This goal is for debugging delete functionality",
            "category": "Debug"
        }
        
        response = requests.post(
            f"{base_url}/goals",
            headers={"Content-Type": "application/json"},
            data=json.dumps(goal_data)
        )
        
        if response.status_code == 200:
            goal = response.json()
            goal_id = goal['id']
            print(f"✅ Created goal with ID: {goal_id}")
        else:
            print(f"❌ Failed to create goal: {response.status_code}")
            print(f"Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error creating goal: {e}")
        return
    
    # Step 3: Verify goal exists
    print(f"\n🔍 Verifying goal {goal_id} exists...")
    try:
        response = requests.get(f"{base_url}/goals/{goal_id}")
        if response.status_code == 200:
            print("✅ Goal exists and is accessible")
        else:
            print(f"❌ Goal not found: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error checking goal: {e}")
        return
    
    # Step 4: Test delete endpoint
    print(f"\n🗑️ Testing delete endpoint for goal {goal_id}...")
    try:
        response = requests.delete(f"{base_url}/goals/{goal_id}")
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Delete successful: {result}")
        else:
            print(f"❌ Delete failed: {response.status_code}")
            print(f"Response body: {response.text}")
            
            # Try to get more details
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print("Could not parse error response as JSON")
                
    except Exception as e:
        print(f"❌ Error during delete: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Verify goal was deleted
    print(f"\n🔍 Verifying goal {goal_id} was deleted...")
    try:
        response = requests.get(f"{base_url}/goals/{goal_id}")
        if response.status_code == 404:
            print("✅ Goal successfully deleted (404 as expected)")
        elif response.status_code == 200:
            print("❌ Goal still exists after deletion!")
        else:
            print(f"❓ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verifying deletion: {e}")
    
    print("\n🎯 Debug complete!")

if __name__ == "__main__":
    debug_delete_issue()