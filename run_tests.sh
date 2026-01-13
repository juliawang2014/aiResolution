#!/bin/bash

# Goal Tracker Test Runner
# Runs all tests from project root

echo "🧪 Goal Tracker Test Suite"
echo "=========================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Change to tests directory and run tests
cd tests
python run_tests.py

echo ""
echo "📋 Available individual tests:"
echo "  Database:     python tests/api/test_simple_db.py"
echo "  Delete Only:  python tests/api/test_delete_only.py"
echo "  API (server): python tests/api/test_api.py"
echo "  Debug:        python tests/api/debug_delete_issue.py"
echo "  Start Server: python tests/debug/debug_start.py"
echo ""
echo "📁 Frontend test: open tests/frontend/test_frontend_delete.html"