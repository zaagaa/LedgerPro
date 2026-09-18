@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: === CONFIG ===
set "PROJECT_NAME=LedgerPro"
set "CURRENT_DIR=%~dp0"
for %%F in ("%CURRENT_DIR:~0,-1%") do set "CURRENT_FOLDER=%%~nxF"

set "PROJECT_DIR=%CURRENT_DIR%"
set "PYTHON_EXE=%PROJECT_DIR%.venv\Scripts\python.exe"
set "DJANGO_PORT=8000"

:: === STEP 0: KILL DJANGO SERVER IF RUNNING ===
echo [INFO] 🔍 Checking if Django server is running on port %DJANGO_PORT%...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%DJANGO_PORT% ^| findstr LISTENING') do (
    echo [INFO] ❌ Server already running. Killing PID %%a...
    taskkill /PID %%a /F >nul 2>&1
    echo [INFO] ✅ Process %%a killed.
)

:: === STEP 1: CHECK IF PARENT FOLDER IS "LedgerPro" ===
echo [INFO] 📁 Current folder: %CURRENT_FOLDER%
if /I not "%CURRENT_FOLDER%"=="LedgerPro" (
    echo [INFO] 🔒 Not in LedgerPro folder. Skipping Git. Running server only...
    goto runserver
)

:: === STEP 2: CHECK INTERNET CONNECTION ===
echo [INFO] 🌐 Checking internet connection...
ping -n 2 8.8.8.8 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] ❌ No internet. Skipping Git update.
    goto runserver
)

:: === STEP 3: GIT FETCH + FORCE UPDATE ===
pushd "%PROJECT_DIR%"
echo [INFO] 🔄 Performing Git update in %PROJECT_DIR%...

if not exist ".git" (
    echo [WARN] ⚠️ No .git folder found. Skipping Git update.
    popd
    goto runserver
)

git rev-parse --verify HEAD >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] ⚠️ Git HEAD not valid. Skipping update.
    popd
    goto runserver
)

for /f %%i in ('git rev-parse HEAD') do set "LOCAL_HASH=%%i"
git fetch origin
for /f %%i in ('git rev-parse origin/main') do set "REMOTE_HASH=%%i"

echo [DEBUG] LOCAL_HASH = !LOCAL_HASH!
echo [DEBUG] REMOTE_HASH = !REMOTE_HASH!

if /I "!LOCAL_HASH!" NEQ "!REMOTE_HASH!" (
    echo [INFO] 🆕 Update found. Forcing pull...

    if exist ".git\index.lock" (
        echo [WARN] ⚠️ Found stale Git lock. Removing...
        del /f /q ".git\index.lock"
    )

    git reset --hard origin/main
    git clean -fd

    echo [INFO] 📦 Installing dependencies...
    "%PYTHON_EXE%" -m pip install -r requirements.txt

    echo [INFO] ⚙️ Applying Django migrations...
    "%PYTHON_EXE%" manage.py migrate
) else (
    echo [INFO] ✅ Repo is already up to date.
)
popd

:: === STEP 4: RUN DJANGO SERVER ===
:runserver
cd /d "%PROJECT_DIR%"
echo [INFO] 🚀 Launching Django development server...
"%PYTHON_EXE%" manage.py runserver 0.0.0.0:%DJANGO_PORT%"
