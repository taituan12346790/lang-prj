#!/usr/bin/env python3
"""
Simple startup test for the backend.
Run this to test if backend starts correctly.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 70)
print("BACKEND STARTUP TEST")
print("=" * 70)

# Test 1: Imports
print("\n[1] Checking imports...")
try:
    import uvicorn
    from app.main import app
    print("    [OK] All imports successful")
except Exception as e:
    print(f"    [ERROR] Import failed: {e}")
    sys.exit(1)

# Test 2: Environment
print("\n[2] Checking environment...")
try:
    from app.core.config import settings
    print(f"    Environment: {settings.ENVIRONMENT}")
    print(f"    Debug: {settings.DEBUG}")
    print(f"    Database: {settings.DATABASE_URL[:30]}...")
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 3: Graceful startup
print("\n[3] Starting server...")
print("    [INFO] Server will start on http://127.0.0.1:8000")
print("    [INFO] API docs: http://127.0.0.1:8000/docs")
print("    [INFO] Press Ctrl+C to stop\n")

try:
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )
except KeyboardInterrupt:
    print("\n\n[INFO] Server stopped by user")
except Exception as e:
    print(f"\n[ERROR] Server failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
