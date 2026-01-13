# 🎯 Goal Tracker

A comprehensive goal tracking system with natural language processing and real-time public dashboard. Set goals, track progress with natural language updates, and get AI-powered feedback to stay motivated and achieve your objectives.

## ✨ Features

- **Smart Goal Setting**: Create goals with categories, descriptions, and target dates
- **Natural Language Updates**: Log progress using everyday language - "I completed 3 chapters today!"
- **AI-Powered Feedback**: Get intelligent insights and motivation based on your updates
- **Real-time Dashboard**: Public dashboard with live updates via WebSocket
- **Progress Analytics**: Visual charts showing progress over time and category breakdowns
- **Sentiment Analysis**: Track your emotional journey toward your goals
- **Mobile Responsive**: Works perfectly on all devices

## 🏗️ Architecture

- **Backend**: Python FastAPI with NLP processing
- **Frontend**: Next.js React dashboard with TypeScript
- **Database**: SQLite with SQLAlchemy ORM (easily upgradeable to PostgreSQL)
- **NLP**: Custom rule-based processor (extensible to spaCy/transformers)
- **Real-time**: WebSocket connections for live updates
- **Styling**: Tailwind CSS with custom components
- **Deployment**: Docker containers with multi-stage builds

## 🧪 Testing

### Run All Tests
```bash
# Automated test runner
./run_tests.sh

# Or manually
cd tests
python run_tests.py
```

### Individual Tests
```bash
# Database connection
python tests/api/test_simple_db.py

# Delete functionality
python tests/api/test_delete_only.py

# API endpoints (requires server running)
python tests/api/test_api.py

# Debug delete issues
python tests/api/debug_delete_issue.py

# Start debug server
python tests/debug/debug_start.py
```

### Frontend Testing
```bash
# Open in browser for manual testing
open tests/frontend/test_frontend_delete.html
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
./scripts/start.sh

# In one terminal - Start backend
source venv/bin/activate
uvicorn app.main:app --reload

# In another terminal - Start frontend  
npm run dev
```

### Option 2: Manual Setup
```bash
# 1. Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node.js dependencies
npm install

# 4. Start backend (Terminal 1)
uvicorn app.main:app --reload

# 5. Start frontend (Terminal 2)
npm run dev
```

### Option 3: Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# For development with hot reload
docker-compose --profile dev up
```

## 🎯 Usage

1. **Access the Dashboard**: Open http://localhost:3000
2. **Create Your First Goal**: Click "Add Goal" and fill in the details
3. **Track Progress**: Click "Add Progress Update" on any goal card
4. **Use Natural Language**: Write updates like:
   - "I completed 50% of my Spanish lessons today and feel great!"
   - "Struggling with motivation this week, only did 2 out of 5 planned workouts"
   - "Finished 3 chapters of my book - that's 8 books down, 16 to go!"
5. **Get AI Feedback**: The system analyzes your updates and provides personalized feedback
6. **Monitor Analytics**: View your progress trends and category breakdowns

## 📊 API Endpoints

### Goals
- `GET /goals` - List all goals
- `POST /goals` - Create new goal
- `GET /goals/{id}` - Get specific goal
- `POST /goals/{id}/update` - Add progress update (natural language)

### Dashboard
- `GET /dashboard` - Public dashboard data with statistics
- `WebSocket /ws` - Real-time updates

### Example API Usage
```bash
# Create a goal
curl -X POST "http://localhost:8000/goals" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Python",
    "description": "Master Python programming",
    "category": "Education",
    "target_date": "2024-12-31"
  }'

# Add progress update
curl -X POST "http://localhost:8000/goals/1/update" \
  -H "Content-Type: application/json" \
  -d '{"text": "Completed 3 coding exercises today, feeling confident!"}'
```

## 🧠 Natural Language Processing

The system intelligently analyzes your progress updates to extract:

- **Progress Percentage**: From explicit percentages, fractions, or contextual clues
- **Sentiment**: Positive, negative, or neutral emotional tone
- **Key Insights**: Important patterns and milestones
- **AI Feedback**: Personalized motivation and suggestions

### Example Analysis
**Input**: "I completed 3 out of 10 chapters today and feel amazing about my progress!"

**Output**:
- Progress: 30%
- Sentiment: Positive
- Insights: ["Reached an important milestone"]
- Feedback: "Excellent progress! Your positive attitude is a great asset for achieving this goal."

## 🎨 Customization

### Adding New Categories
Edit the category options in `components/AddGoalForm.tsx`:
```typescript
<option value="Your Category">Your Category</option>
```

### Extending NLP Analysis
Modify `app/nlp_processor.py` to add new keywords or analysis patterns:
```python
self.progress_keywords = {
    "high": ["completed", "finished", "achieved"],
    # Add your keywords
}
```

### Styling
Customize the design by editing `styles/globals.css` and Tailwind classes.

## 🚢 Deployment

### Production Docker Build
```bash
# Build production image
docker build -t goal-tracker .

# Run production container
docker run -p 8000:8000 -v $(pwd)/data:/app/data goal-tracker
```

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
DATABASE_URL=sqlite:///./goals.db
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Sample Data

Generate sample goals and progress entries:
```bash
python scripts/sample_data.py
```

This creates 5 example goals with realistic progress updates to demonstrate the system.

## 📦 Dependencies

### Backend (Python)
- **FastAPI** - Modern web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **WebSockets** - Real-time communication
- **Uvicorn** - ASGI server

### Frontend (React/Next.js)
- **Next.js** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **date-fns** - Date utilities

## 🔧 Development
```
├── app/                    # FastAPI backend
│   ├── main.py            # API routes and WebSocket
│   ├── models.py          # Database models
│   ├── schemas.py         # Pydantic schemas
│   ├── crud.py            # Database operations
│   ├── nlp_processor.py   # Natural language processing
│   └── websocket_manager.py # WebSocket handling
├── components/            # React components
├── pages/                 # Next.js pages
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript type definitions
├── styles/                # CSS and styling
└── scripts/               # Utility scripts
```

### Adding New Features
1. **Backend**: Add routes in `app/main.py`, models in `app/models.py`
2. **Frontend**: Create components in `components/`, add pages in `pages/`
3. **Database**: Update models and run migrations
4. **Real-time**: Use WebSocket manager for live updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**Port already in use**:
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Database issues**:
```bash
# Delete and recreate database
rm goals.db
python -c "from app.database import engine; from app import models; models.Base.metadata.create_all(bind=engine)"
```

**WebSocket connection failed**:
- Ensure backend is running on port 8000
- Check firewall settings
- Verify WebSocket URL in frontend code

## 🎉 What's Next?

- [ ] User authentication and personal dashboards
- [ ] Goal sharing and social features
- [ ] Advanced NLP with spaCy integration
- [ ] Mobile app with React Native
- [ ] Email/SMS reminders and notifications
- [ ] Integration with calendar apps
- [ ] Export data to PDF reports
- [ ] Goal templates and recommendations

---

**Ready to achieve your goals?** 🚀 Start tracking today!