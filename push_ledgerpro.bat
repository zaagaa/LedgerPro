@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: === CONFIG ===
set "FOLDER=LedgerPro"
set "REPO_URL=https://github.com/zaagaa/LedgerPro.git"
set "BRANCH=main"
set "SCRIPT_DIR=%~dp0"
set "FOLDER_PATH=%SCRIPT_DIR%%FOLDER%"

:: === CHECK IF CURRENT DIR IS THE FOLDER ===
pushd "%SCRIPT_DIR%" >nul
for %%F in (.) do set "CURRENT_DIR=%%~nxF"

IF /I "%CURRENT_DIR%"=="%FOLDER%" (
    set "TARGET_DIR=%SCRIPT_DIR%"
) ELSE (
    IF EXIST "%FOLDER_PATH%\" (
        set "TARGET_DIR=%FOLDER_PATH%"
    ) ELSE (
        echo [ERROR] ❌ Folder "%FOLDER%" not found in "%SCRIPT_DIR%"
        pause
        exit /b 1
    )
)

:: === MOVE INTO TARGET DIR ===
cd /d "%TARGET_DIR%"

:: === INITIALIZE GIT IF NEEDED ===
IF NOT EXIST ".git" (
    echo [INFO] 🧱 Initializing new Git repo...
    git init
    git remote add origin %REPO_URL%
)

:: === GET VERSION FROM version.txt ===
set "VERSION_FILE=version.txt"
IF NOT EXIST "%VERSION_FILE%" set "VERSION_FILE=version.txt"

IF EXIST "%VERSION_FILE%" (
    for /f "usebackq delims=" %%v in ("%VERSION_FILE%") do set "VERSION=%%v"
    echo [INFO] 📌 Version: %VERSION%
) ELSE (
    echo [WARNING] ⚠️ version.txt not found. Skipping tag...
    set "VERSION="
)

:: === STAGE AND COMMIT ===
echo [INFO] 🔄 Staging changes...
git add .

echo [INFO] 📝 Committing changes...
git commit -m "Auto update @ %DATE% %TIME%" >nul 2>&1

:: === FORCE PUSH ===
echo [INFO] ☠️ Force pushing to %BRANCH%...
git branch -M %BRANCH%
git push -f origin %BRANCH%

:: === TAG PUSH (if version found) ===
IF DEFINED VERSION (
    git tag -f v%VERSION%
    git push -f origin v%VERSION%
    echo [INFO] 🔖 Tagged as v%VERSION% and pushed.
)

echo.
echo ✅ Push complete!

