from app.config import settings
import os

print(f"GOOGLE_CLIENT_ID set: {bool(settings.GOOGLE_CLIENT_ID)}")
print(f"GOOGLE_CLIENT_SECRET set: {bool(settings.GOOGLE_CLIENT_SECRET)}")
print(f"BACKEND_URL: {settings.BACKEND_URL}")
print(f"Redirect URI: {settings.BACKEND_URL}/auth/google/callback")
