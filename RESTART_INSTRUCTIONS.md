# How to Restart the Backend Server

The backend server needs to be restarted to pick up the changes for:
1. Fixed flowchart generation (better markdown cleaning)
2. New `/auth/profile` endpoint for settings page

## Steps to Restart Backend:

### Option 1: With Auto-Reload (Recommended for Development)
```bash
cd backend
source .venv/bin/activate  # or: .venv/bin/activate (depending on shell)
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag will automatically restart the server when you make code changes.

### Option 2: Without Auto-Reload (Production)
```bash
cd backend
source .venv/bin/activate
uvicorn app.server:app --host 0.0.0.0 --port 8000
```

## Verify Backend is Running

Check that the server is responding:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"AI CodeDoc Studio API"}
```

## Test the New Endpoints

### Test Profile Endpoint (requires authentication)
```bash
# Get your auth token from browser localStorage (key: 'auth_token')
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/auth/profile
```

### Test Flowchart Generation
```bash
# Use the frontend at http://localhost:3000/page/flowchart
# Or use the test script:
cd backend
python test_flowchart.py
```

## Frontend Should Already Be Running

The Next.js frontend should still be running on port 3000. If not:
```bash
cd /home/rht/Pro/ai-code-doc
npm run dev
```

## What's Fixed

1. **Flowchart Generation**: Now uses regex-based cleaning to remove ALL markdown code blocks
2. **Settings Page**: Can now fetch user profile data from `/auth/profile`
3. **Better Logging**: Backend logs show raw and cleaned Mermaid code for debugging
