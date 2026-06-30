"""Test router directly without running server"""
from fastapi import FastAPI
from app.routers import learning_path

app = FastAPI()

print(f"Router object: {learning_path.router}")
print(f"Router prefix: {learning_path.router.prefix}")
print(f"Router routes: {len(learning_path.router.routes)}")
print("\nRoutes:")
for route in learning_path.router.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        print(f"  {list(route.methods)} {route.path}")

# Try to include it
app.include_router(learning_path.router)

print(f"\nApp routes after including:")
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        print(f"  {list(route.methods)} {route.path}")
