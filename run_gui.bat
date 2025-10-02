@echo off
REM -------------------------------
REM Secure Deletion Tool - GUI Launcher
REM -------------------------------

REM Navigate to script folder
cd /d %~dp0

REM Activate virtual environment (if you used .venv)
call .venv\Scripts\activate

REM Run GUI
python -m src.gui

REM Pause so user can see any messages
pause
