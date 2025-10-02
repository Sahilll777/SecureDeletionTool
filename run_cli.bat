@echo off
REM -------------------------------
REM Secure Deletion Tool - CLI Launcher
REM -------------------------------

REM Navigate to script folder
cd /d %~dp0

REM Activate virtual environment
call .venv\Scripts\activate

REM Show usage instructions
echo Secure Deletion Tool CLI
echo ------------------------
echo Available commands:
echo   wipe [file/folder] --passes N
echo   wipe-free [folder/drive] --passes N --preview
echo   list-drives --removable
echo.
echo Example:
echo   run_cli.bat wipe C:\Temp\test.txt --passes 3
echo.

REM Pass all arguments to Python CLI
python -m src.cli %*

REM Pause so user can see output
pause
 