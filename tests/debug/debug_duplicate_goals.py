#!/usr/bin/env python3
"""
Debug script to identify duplicate goal creation issue
"""

import requests
import json
import time
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

def test_single_goal_creation():
    """Test creating a single goal and check for duplicates"""
    print("🔍 Testing Single Goal Creation")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Get initial goal count
    try:
        response = requests.get(f"{base_url}/goals")
        initial_goals = response.json()
        initial_count = len(initial_goals)
        print(f"📊 Initial goal count: {initial_count}")
    except Exception as e:
        print(f"❌ Failed to get initial goals: {e}")
        return
    
    # Create a single goal
    print("\n📝 Creating single test goal...")
    goal_data = {
        "title": "Duplicate Test Goal",
        "description": "Testing for duplicate creation",
        "category": "Debug"
    }
    
    try:
        response = requests.post(
            f"{base_url}/goals",
            headers={"Content-Type": "application/json"},
            data=json.dumps(goal_data)
        )
        
        if response.status_code == 200:
            created_goal = response.json()
            print(f"✅ Goal created with ID: {created_goal['id']}")
            print(f"📋 Goal title: {created_goal['title']}")
        else:
            print(f"❌ Failed to create goal: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error creating goal: {e}")
        return
    
    # Wait a moment for any async processing
    print("\n⏳ Waiting 2 seconds for processing...")
    time.sleep(2)
    
    # Check final goal count
    try:
        response = requests.get(f"{base_url}/goals")
        final_goals = response.json()
        final_count = len(final_goals)
        print(f"\n📊 Final goal count: {final_count}")
        print(f"📈 Goals added: {final_count - initial_count}")
        
        # Check for duplicates by title
        duplicate_titles = []
        titles_seen = set()
        
        for goal in final_goals:
            if goal['title'] in titles_seen:
                duplicate_titles.append(goal['title'])
            titles_seen.add(goal['title'])
        
        if duplicate_titles:
            print(f"❌ Found duplicate titles: {duplicate_titles}")
            
            # Show all goals with the test title
            test_goals = [g for g in final_goals if g['title'] == goal_data['title']]
            print(f"\n🔍 Goals with title '{goal_data['title']}':")
            for i, goal in enumerate(test_goals, 1):
                print(f"  {i}. ID: {goal['id']}, Created: {goal['created_at']}")
        else:
            print("✅ No duplicate titles found")
        
        if final_count - initial_count == 1:
            print("✅ Exactly 1 goal was added (correct behavior)")
        elif final_count - initial_count > 1:
            print(f"❌ {final_count - initial_count} goals were added (duplicate creation detected!)")
        else:
            print("❓ No goals were added (unexpected)")
            
    except Exception as e:
        print(f"❌ Error checking final goals: {e}")

def test_rapid_goal_creation():
    """Test rapid goal creation to see if it causes duplicates"""
    print("\n\n🚀 Testing Rapid Goal Creation")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Create multiple goals rapidly
    goals_to_create = 3
    created_ids = []
    
    for i in range(goals_to_create):
        goal_data = {
            "title": f"Rapid Test Goal {i+1}",
            "description": f"Rapid creation test #{i+1}",
            "category": "Debug"
        }
        
        try:
            response = requests.post(
                f"{base_url}/goals",
                headers={"Content-Type": "application/json"},
                data=json.dumps(goal_data)
            )
            
            if response.status_code == 200:
                created_goal = response.json()
                created_ids.append(created_goal['id'])
                print(f"✅ Created goal {i+1}: ID {created_goal['id']}")
            else:
                print(f"❌ Failed to create goal {i+1}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error creating goal {i+1}: {e}")
    
    print(f"\n📊 Created {len(created_ids)} goals with IDs: {created_ids}")
    
    # Check if all IDs are unique
    if len(created_ids) == len(set(created_ids)):
        print("✅ All goal IDs are unique")
    else:
        print("❌ Duplicate goal IDs detected!")

def main():
    print("🐛 Duplicate Goals Debug Tool")
    print("=" * 60)
    
    # Test single goal creation
    test_single_goal_creation()
    
    # Test rapid goal creation
    test_rapid_goal_creation()
    
    print("\n" + "=" * 60)
    print("🎯 Debug Complete!")
    print("\nIf duplicates are found:")
    print("1. Check browser console for multiple WebSocket messages")
    print("2. Check if form is submitting multiple times")
    print("3. Check if WebSocket is connecting multiple times")
    print("4. Verify React component re-renders")

if __name__ == "__main__":
    main()