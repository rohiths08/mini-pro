# Quick Fix Guide - Flowchart & Settings Issues

## Issues You're Experiencing

1. **Flowchart Error**: "Invalid mermaid code: \`\`\`mermaid flowchart TD..."
2. **Settings Page 404**: `/auth/profile` endpoint returns 404
3. **Settings Page Empty**: No user data showing

## Root Cause

The backend server needs to be restarted to load the updated code with:
- Improved regex-based markdown cleaning for flowcharts
- New `/auth/profile` endpoint for settings page

## Solution - Restart Backend Server

### Step 1: Stop the Current Backend (if running)

Find and kill the process:
```bash
# Find the process
ps aux | grep uvicorn

# Kill it (replace PID with actual process ID)
kill <PID>
```

### Step 2: Start Backend with Auto-Reload

**Easy way using the script:**
```bash
cd /home/rht/Pro/ai-code-doc/backend
./start_server.sh
```

**Manual way:**
```bash
cd /home/rht/Pro/ai-code-doc/backend
source .venv/bin/activate
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3: Verify Backend is Running

Open a new terminal and test:
```bash
# Test health endpoint
curl http://localhost:8000/health

# Should return: {"status":"healthy","service":"AI CodeDoc Studio API"}
```

### Step 4: Test in Browser

1. **Refresh the frontend** at http://localhost:3000
2. **Go to Settings page** - Should now load user profile
3. **Go to Flowchart page** - Generate a flowchart and check console

## What Was Fixed

### Flowchart Generation (`backend/app/core/flowchart.py`)
- **Old**: Simple string replacement for markdown blocks
- **New**: Regex-based aggressive cleaning that handles:
  - ` ```mermaid ` at start (case insensitive)
  - ` ``` ` at end
  - Standalone ` ``` ` lines
  - Inline backticks
  - Multiple whitespace variations

### Settings Page (`app/settings/page.tsx` + `backend/app/routes/auth_routes.py`)
- **Added**: New `/auth/profile` GET endpoint
- **Returns**: User ID, email, name, picture, created_at
- **Frontend**: Settings page now properly fetches and displays user data

## Expected Results After Restart

### Flowchart Page
Console should show:
```
Received mermaid code: flowchart TD
    A[Start] --> B[Calculate a + b]
    ...
```
Notice: NO backticks at the start!

### Settings Page
Should display:
- Profile picture (if available)
- Name
- Email
- User ID
- Member since date
- Language preferences
- Sign out button

## Still Having Issues?

### Check Backend Logs
The backend now logs detailed info:
```
INFO: Raw AI response (first 200 chars): ...
INFO: Cleaned mermaid code (first 200 chars): ...
```

### Check Browser Console
Look for:
```
Received mermaid code: <should start with 'flowchart' or 'graph'>
```

### Run the Test Script
```bash
cd backend
python test_flowchart.py
```

This will show you exactly what the AI returns and how it's cleaned.

## Common Issues

### Backend won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- Check virtual environment: `source .venv/bin/activate`
- Check dependencies: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Verify backend is on port 8000
- Check CORS settings in `backend/app/server.py`
- Check `FRONTEND_URL` in backend `.env` file

### Profile endpoint still 404
- Verify server restarted: Check timestamp in terminal
- Check routes are loaded: Look for "INFO: Application startup complete" in logs
