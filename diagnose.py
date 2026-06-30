#!/usr/bin/env python3
"""
Quick diagnostic to identify backend startup issues.
Run: python diagnose.py
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "=" * 70)
print("BACKEND DIAGNOSIS TOOL")
print("=" * 70)

issues = []
warnings = []

# Check 1: Python version
print("\n[1] Python Version")
print(f"    Version: {sys.version}")
if sys.version_info < (3, 8):
    issues.append("Python 3.8+ required")
else:
    print("    [OK]")

# Check 2: PostgreSQL
print("\n[2] PostgreSQL Connection")
try:
    result = subprocess.run(['pg_isready', '-h', 'localhost'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("    [OK] PostgreSQL responding")
    else:
        issues.append(f"PostgreSQL not responding: {result.stderr}")
except FileNotFoundError:
    warnings.append("pg_isready not found (PostgreSQL might be installed)")
except Exception as e:
    issues.append(f"PostgreSQL check failed: {e}")

# Check 3: Database
print("\n[3] Database Connection")
try:
    from app.core.config import settings
    print(f"    Database URL: {settings.DATABASE_URL[:40]}...")
    
    # Test connection
    import asyncio
    from sqlalchemy import text
    from app.core.database import engine
    
    async def test_db():
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            return False
    
    result = asyncio.run(test_db())
    if result:
        print("    [OK] Database connection works")
    else:
        issues.append("Cannot connect to database")
except Exception as e:
    issues.append(f"Database error: {e}")

# Check 4: Imports
print("\n[4] Package Imports")
packages = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'asyncpg',
    'authlib',
    'groq',
    'loguru',
    'httpx',
    'starlette'
]

missing = []
for pkg in packages:
    try:
        __import__(pkg)
    except ImportError:
        missing.append(pkg)

if missing:
    issues.append(f"Missing packages: {', '.join(missing)}")
    print(f"    [ERROR] Missing: {', '.join(missing)}")
else:
    print("    [OK] All packages installed")

# Check 5: Environment Variables
print("\n[5] Environment Variables")
required = ['GROQ_API_KEY', 'DATABASE_URL', 'SECRET_KEY']
missing_env = []

for var in required:
    val = os.getenv(var)
    if not val:
        missing_env.append(var)
    else:
        masked = val[:10] + "..." if len(val) > 10 else val
        print(f"    {var}: {masked}")

if missing_env:
    issues.append(f"Missing env vars: {', '.join(missing_env)}")

# Check 6: FastAPI App
print("\n[6] FastAPI App")
try:
    from app.main import app
    print("    [OK] App imports successfully")
    
    # Try test client
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    response = client.get("/health")
    if response.status_code == 200:
        print("    [OK] Health endpoint works")
    else:
        issues.append(f"Health endpoint returned {response.status_code}")
except Exception as e:
    issues.append(f"App error: {e}")

# Check 7: Port
print("\n[7] Port 8000")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 8000))
sock.close()

if result == 0:
    warnings.append("Port 8000 already in use (server might be running)")
else:
    print("    [OK] Port 8000 available")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if issues:
    print(f"\nISSUES FOUND ({len(issues)}):")
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. {issue}")

if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for i, warning in enumerate(warnings, 1):
        print(f"  {i}. {warning}")

if not issues:
    print("\nAll checks passed! Backend should start.")
    print("\nTo start backend:")
    print("  python run_backend.py")
    print("  or")
    print("  python -m uvicorn app.main:app --reload")
else:
    print("\nFix issues above before starting backend.")

print("=" * 70 + "\n")
