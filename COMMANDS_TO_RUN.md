# Commands to Run Right Now

Copy and paste these commands in your terminal to fix the issues:

## 1. Stop the Old Backend Server

```bash
pkill -f "uvicorn app.server:app"
```

## 2. Start the New Backend Server

```bash
cd /home/rht/Pro/ai-code-doc/backend && ./start_server.sh
```

**OR if the script doesn't work:**

```bash
cd /home/rht/Pro/ai-code-doc/backend
source .venv/bin/activate
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```

## 3. Verify Backend is Working

Open a **new terminal** and run:

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{"status":"healthy","service":"AI CodeDoc Studio API"}
```

## 4. Refresh Your Browser

Go to: http://localhost:3000

## 5. Test the Fixes

### Test Settings Page:
1. Navigate to Settings (bottom of sidebar)
2. You should see your profile information

### Test Flowchart:
1. Navigate to Flowchart page
2. Click "Submit" to generate a flowchart
3. Open browser console (F12)
4. Look for: `Received mermaid code: flowchart TD`
5. The flowchart should render without errors

## Troubleshooting

If backend won't start:
```bash
# Check what's using port 8000
lsof -i :8000

# Kill it if needed
kill -9 <PID>

# Then restart backend
cd /home/rht/Pro/ai-code-doc/backend
source .venv/bin/activate
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```

## Summary of What Changed

✅ **Flowchart**: Better regex cleaning removes ALL markdown formatting
✅ **Settings**: New `/auth/profile` endpoint returns user data
✅ **Logging**: Backend now shows raw and cleaned Mermaid code
✅ **Frontend**: Better error handling and validation

The key issue was that the backend server was running the OLD code. Restarting it loads the NEW fixed code.
