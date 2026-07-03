"""Test to see all registered routes"""
from app.main import app

print("📋 All registered routes:\n")

for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        methods = ','.join(route.methods)
        print(f"  {methods:10} {route.path}")

print("\n✅ Routes listed")
