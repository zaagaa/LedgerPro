@echo off
SETLOCAL

echo [INFO] Creating virtual environment in ".venv"...
python -m venv .venv

IF NOT EXIST ".venv\Scripts\activate.bat" (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)

echo [INFO] Installing packages from requirements.txt...
pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Package installation failed.
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment is ready with all packages installed!
pause
