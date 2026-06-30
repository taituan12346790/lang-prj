@echo off
echo Running Alembic migration 007 - Add chat_learning_activities table...
echo.

REM Activate virtual environment if exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Run migration
alembic upgrade head

echo.
echo Migration completed!
echo.
pause
