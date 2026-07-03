@echo off
echo Xoa cac file khong can thiet khoi Git repository (giu lai tren local)...
echo.

REM Xoa cac file .txt (ngoai tru requirements.txt va runtime.txt)
git rm --cached *.txt 2>nul
git rm --cached "user data/*.txt" 2>nul

REM Them lai cac file can thiet
git add requirements.txt 2>nul
git add requirements-streamlit.txt 2>nul
git add runtime.txt 2>nul
git add packages.txt 2>nul

REM Xoa cac file .md (ngoai tru README.md)
for %%f in (*.md) do (
    if not "%%f"=="README.md" (
        git rm --cached "%%f" 2>nul
    )
)

REM Xoa cac file .pdf va .docx
git rm --cached *.pdf 2>nul
git rm --cached *.docx 2>nul

REM Xoa cac file test
git rm --cached test_*.py 2>nul
git rm --cached *_test.py 2>nul

REM Xoa cac file script tien ich
git rm --cached vietnamize*.py 2>nul
git rm --cached fix_*.py 2>nul
git rm --cached extract_*.py 2>nul
git rm --cached check_*.py 2>nul
git rm --cached split_*.py 2>nul
git rm --cached update_*.py 2>nul
git rm --cached final_*.py 2>nul
git rm --cached complete_*.py 2>nul
git rm --cached auto_*.py 2>nul
git rm --cached validate_*.py 2>nul
git rm --cached verify_*.py 2>nul
git rm --cached debug_*.py 2>nul
git rm --cached diagnose.py 2>nul
git rm --cached translate_*.py 2>nul

REM Xoa cac file backup
git rm --cached *.backup 2>nul
git rm --cached *.bak 2>nul
git rm --cached *_DEMO_*.py 2>nul
git rm --cached topic_*_edited.py 2>nul
git rm --cached topic_*_original.txt 2>nul
git rm --cached topics_data_DEMO*.py 2>nul

REM Xoa file HTML test
git rm --cached test_oauth.html 2>nul

REM Xoa file Python khong can thiet
git rm --cached a.py 2>nul
git rm --cached config.py 2>nul
git rm --cached run_backend.py 2>nul
git rm --cached run_migration*.py 2>nul
git rm --cached run_migration*.bat 2>nul
git rm --cached seed_*.py 2>nul
git rm --cached reseed_*.py 2>nul
git rm --cached init_db.py 2>nul
git rm --cached add_writing_lessons*.py 2>nul

REM Xoa cac file streamlit backup
git rm --cached streamlit_app*.backup 2>nul
git rm --cached streamlit_app_chat_only.py 2>nul
git rm --cached streamlit_app_redesigned.py 2>nul

REM Xoa bat files
git rm --cached start_system.bat 2>nul
git rm --cached stop_system.bat 2>nul

echo.
echo Hoan thanh! Cac file da duoc xoa khoi Git tracking nhung van con tren local.
echo Ban co the xem trang thai voi lenh: git status
echo.
pause
