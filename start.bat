@echo off
cd /d "%~dp0"
title XYZ Company sign-up

where py >nul 2>&1
if %errorlevel%==0 goto runpy
where python >nul 2>&1
if %errorlevel%==0 goto runpython

echo Python was not found.
echo.
echo 1. Open https://www.python.org/downloads/windows/
echo 2. Install Python 3.
echo 3. On the first screen, check the box Add python.exe to PATH.
echo 4. Double-click start.bat again.
echo.
pause
exit /b 1

:runpy
echo Leave this window open. Closing it stops the website.
echo.
py server.py --open
echo.
echo The website has stopped.
pause
exit /b 0

:runpython
echo Leave this window open. Closing it stops the website.
echo.
python server.py --open
echo.
echo The website has stopped.
pause
exit /b 0
