# 🧪 Goal Tracker Tests

This folder contains all testing and debugging utilities for the Goal Tracker application.

## 📁 Test Structure

```
tests/
├── README.md                           # This file
├── __init__.py                        # Python package init
├── api/                               # API testing
│   ├── test_api.py                   # Complete API test suite
│   ├── test_simple_db.py             # Database connection tests
│   ├── test_delete_only.py           # Isolated delete functionality test
│   └── debug_delete_issue.py         # Delete issue debugging
├── frontend/                          # Frontend testing
│   └── test_frontend_delete.html     # Simple HTML delete test
├── debug/                             # Debug utilities
│   └── debug_start.py                # Debug server startup
└── docs/                              # Test documentation
    ├── DELETE_FEATURE.md              # Delete feature documentation
    └── TROUBLESHOOTING_DELETE.md      # Delete troubleshooting guide
```

## 🚀 Quick Test Commands

### Run All Tests
```bash
# From project root
cd tests
python -m pytest api/ -v
```

### Test Database
```bash
cd tests
python api/test_simple_db.py
```

### Test API Endpoints
```bash
cd tests
python api/test_api.py
```

### Debug Delete Issues
```bash
cd tests
python api/debug_delete_issue.py
```

### Test Frontend (Manual)
```bash
# Open in browser
open frontend/test_frontend_delete.html
```

### Start Debug Server
```bash
cd tests
python debug/debug_start.py
```

## 📋 Test Categories

### Unit Tests
- Database connection and models
- CRUD operations
- Schema validation

### Integration Tests
- API endpoints
- WebSocket functionality
- Real-time updates

### Frontend Tests
- Delete functionality
- Modal interactions
- API communication

### Debug Tools
- Server startup with logging
- Issue-specific debugging
- Performance monitoring

## 🔧 Test Configuration

All tests are configured to work from the project root. The test scripts automatically adjust their Python path to import the main application modules.

## 📊 Test Coverage

- ✅ Database operations (CRUD)
- ✅ API endpoints (all routes)
- ✅ Delete functionality (backend)
- ✅ WebSocket communication
- ✅ Error handling
- ⏳ Frontend UI testing (manual)
- ⏳ End-to-end testing

## 🐛 Debugging Workflow

1. **Database Issues**: Run `api/test_simple_db.py`
2. **API Issues**: Run `api/test_api.py`
3. **Delete Issues**: Run `api/debug_delete_issue.py`
4. **Frontend Issues**: Open `frontend/test_frontend_delete.html`
5. **Server Issues**: Use `debug/debug_start.py`

## 📝 Adding New Tests

### API Tests
Add new test functions to `api/test_api.py` or create new files in the `api/` folder.

### Frontend Tests
Create new HTML files in `frontend/` folder for manual testing or add automated tests.

### Debug Tools
Add new debugging scripts to `debug/` folder.

---

**All tests are designed to be run independently and don't require external dependencies beyond the main application requirements.**