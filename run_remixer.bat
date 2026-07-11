 @echo off
echo Video Remixer inditasa...
echo.

REM Ellenorizze, hogy telepitve van-e Python
python --version >nul 2>&1
if errorlevel 1 (
    echo HIBA: Python nincs telepítve vagy nincs a PATH-ban!
    echo Töltse le innen: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Telepitsd a szukseges csomagokat (elso futasra)
echo Szukseges csomagok telepitese...
pip install -r requirements.txt

REM Futtasd a remixert
echo.
echo A program inditasa...
echo.
echo Ha van YouTube URL-ed, add meg parameterkent:
echo   run_remixer.bat "https://www.youtube.com/watch?v=..."
echo.
echo Vagy nyomj Enter-t, hogy beird kesobb...
echo.

python video_remixer.py %1

pause