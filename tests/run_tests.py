#!/usr/bin/env python3
"""
Test runner for Goal Tracker
Runs all tests in the correct order with proper setup
"""

import sys
import os
import subprocess
import time

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def run_command(cmd, description, cwd=None):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    try:
        if cwd:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("🧪 Goal Tracker Test Suite")
    print("=" * 60)
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    results = []
    
    # Test 1: Database Connection
    results.append(run_command(
        "python api/test_simple_db.py",
        "Database Connection Test"
    ))
    
    # Test 2: Delete Functionality (isolated)
    results.append(run_command(
        "python api/test_delete_only.py", 
        "Delete Functionality Test"
    ))
    
    # Test 3: API Endpoints (requires server)
    print("\n⚠️  API tests require the server to be running on port 8000")
    print("   Start server with: python debug/debug_start.py")
    
    server_test = input("\nRun API tests? (y/N): ").lower().strip()
    if server_test == 'y':
        results.append(run_command(
            "python api/test_api.py",
            "API Endpoints Test"
        ))
        
        results.append(run_command(
            "python api/debug_delete_issue.py",
            "Delete Issue Debug Test"
        ))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, result in enumerate(results, 1):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"Test {i}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed. Check output above for details.")
        return 1

if __name__ == "__main__":
    exit(main())