#!/bin/bash

# Goal Tracker Startup Script

echo "🎯 Starting Goal Tracker..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Create data directory
mkdir -p data

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   Backend:  uvicorn app.main:app --reload"
echo "   Frontend: npm run dev"
echo ""
echo "📊 Dashboard will be available at: http://localhost:3000"
echo "🔌 API will be available at: http://localhost:8000"