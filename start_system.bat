@echo off
echo ========================================
echo   AI LANGUAGE TUTOR - STARTING SYSTEM
echo ========================================
echo.

echo [1/3] Killing old Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] Starting Backend Server...
start "Backend - Uvicorn" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 8 /nobreak >nul

echo [3/3] Starting Frontend (Streamlit)...
start "Frontend - Streamlit" cmd /k "streamlit run streamlit_app.py"

echo.
echo ========================================
echo   SYSTEM STARTED SUCCESSFULLY!
echo ========================================
echo.
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:8501
echo API Docs: http://127.0.0.1:8000/docs
echo.
echo Press any key to exit this window...
pause >nul
