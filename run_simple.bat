 @echo off
echo SIMPLE VIDEO DOWNLOADER
echo ======================
echo.

REM Python ellenőrzés
python --version >nul 2>&1
if errorlevel 1 (
    echo HIBA: Python nincs telepítve!
    pause
    exit /b 1
)

REM Csomagok telepítése
echo Csomagok telepitese...
pip install yt-dlp >nul 2>&1

REM Program futtatása
echo.
echo Program inditasa...
echo.
echo Hasznalat:
echo   run_simple.bat
echo   VAGY
echo   run_simple.bat "https://www.youtube.com/watch?v=..."
echo.

if "%~1"=="" (
    python simple_video_downloader.py
) else (
    python simple_video_downloader.py "%~1"
)

pause