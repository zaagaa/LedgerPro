@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: === CONFIG ===
SET PYTHON_VERSION=3.12.1
SET PYTHON_FOLDER=Python312
SET PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
SET INSTALLER=python-installer.exe

SET REPO_URL=https://github.com/zaagaa/LedgerPro.git
SET BRANCH_NAME=main
SET PROJECT_FOLDER=LedgerPro
SET GIT_VERSION=2.44.0
SET SERVER_URL=http://127.0.0.1:8000

:: === STEP 1: CHECK PYTHON ===
SET PYTHON_EXEC=
FOR /F "usebackq delims=" %%i IN (`where python 2^>nul`) DO (
    %%i --version >nul 2>&1
    IF !ERRORLEVEL! EQU 0 (
        SET PYTHON_EXEC=%%i
        GOTO python_ok
    )
)

IF EXIST "C:\Program Files\%PYTHON_FOLDER%\python.exe" (
    SET PYTHON_EXEC="C:\Program Files\%PYTHON_FOLDER%\python.exe"
    GOTO python_ok
)
IF EXIST "%LocalAppData%\Programs\%PYTHON_FOLDER%\python.exe" (
    SET PYTHON_EXEC="%LocalAppData%\Programs\%PYTHON_FOLDER%\python.exe"
    GOTO python_ok
)

echo [INFO] Python not found.
IF EXIST %INSTALLER% (
    echo [INFO] Using existing Python installer.
) ELSE (
    echo [INFO] Downloading Python installer...
    curl -L -o %INSTALLER% %PYTHON_URL%
    IF NOT EXIST %INSTALLER% (
        echo [ERROR] Python download failed.
        pause
        exit /b 1
    )
)

powershell -Command "Write-Host '[INFO] Installing Python...' -NoNewline; Write-Host ' Please click \"Yes\" on the security popup.' -ForegroundColor Yellow"
start "" /b "%INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Wait until python installer starts
:wait_python_start
timeout /t 1 >nul
tasklist | findstr /i "python-installer.exe" >nul
if errorlevel 1 goto wait_python_start

:: Spinner while Python is installing
set "spinner=\|/-"
set /a counter=0
echo.
:spinner_python
set /a index=counter %% 4
set "ch=!spinner:~%index%,1!"
<nul set /p=Installing Python... !ch!
ping -n 2 127.0.0.1 >nul
<nul set /p=[2K[G
set /a counter+=1
tasklist | findstr /i "python-installer.exe" >nul
if not errorlevel 1 goto spinner_python

echo.
echo [INFO] Python installation complete.
del /f /q %INSTALLER%

:: === FORCE RESTART SCRIPT TO REFRESH PATH ===
IF "%RESTARTED%" NEQ "1" (
    set RESTARTED=1
    echo [INFO] Restarting script after Python install...
    start "" "%~f0" RESTARTED=1
    exit /b
)

:python_ok
echo [INFO] Using Python at: %PYTHON_EXEC%

:: === STEP 2: CHECK GIT ===
where git >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] Git not found.
    IF EXIST git-installer.exe (
        echo [INFO] Using existing Git installer.
    ) ELSE (
        echo [INFO] Downloading Git installer...
        curl -L -o git-installer.exe https://github.com/git-for-windows/git/releases/download/v%GIT_VERSION%.windows.1/Git-%GIT_VERSION%-64-bit.exe
        IF NOT EXIST git-installer.exe (
            echo [ERROR] Git download failed.
            pause
            exit /b 1
        )
    )

    powershell -Command "Write-Host '[INFO] Installing Git...' -NoNewline; Write-Host ' Please click \"Yes\" on the security popup.' -ForegroundColor Yellow"
    start "" /b git-installer.exe /VERYSILENT /NORESTART

    :wait_git_start
    timeout /t 1 >nul
    tasklist | findstr /i "git-installer.exe" >nul
    if errorlevel 1 goto wait_git_start

    set "spinner=\|/-"
    set /a counter=0
    echo.
    :spinner_git
    set /a index=counter %% 4
    set "ch=!spinner:~%index%,1!"
    <nul set /p=Installing Git... !ch!
    ping -n 2 127.0.0.1 >nul
    <nul set /p=[2K[G
    set /a counter+=1
    tasklist | findstr /i "git-installer.exe" >nul
    if not errorlevel 1 goto spinner_git

    echo.
    echo [INFO] Git installation complete.
)

:: === RECHECK GIT ===
where git >nul 2>&1
IF ERRORLEVEL 1 (
    SET "GIT_PATH=C:\Program Files\Git\bin\git.exe"
    IF EXIST "%GIT_PATH%" (
        echo [INFO] Git found manually at %GIT_PATH%
        setx PATH "%PATH%;C:\Program Files\Git\cmd" >nul
        set "GIT_CMD=%GIT_PATH%"
    ) ELSE (
        echo [ERROR] Git still not found after install.
        IF "%RESTARTED%"=="2" (
            echo [FATAL] Git not usable. Aborting.
            pause
            exit /b 1
        ) ELSE (
            echo [INFO] Restarting script after Git install...
            set RESTARTED=2
            start "" "%~f0" RESTARTED=2
            exit /b
        )
    )
) ELSE (
    set "GIT_CMD=git"
    echo [INFO] Git is ready.
)

:: === STEP 3: CLONE PROJECT ===
IF NOT EXIST %PROJECT_FOLDER% (
    echo [INFO] Cloning project...
    %GIT_CMD% clone -b %BRANCH_NAME% %REPO_URL%
    IF ERRORLEVEL 1 (
        echo [ERROR] Git clone failed.
        pause
        exit /b 1
    )
) ELSE (
    echo [INFO] Project folder already exists.
)

IF EXIST git-installer.exe del /f /q git-installer.exe

cd /d "%~dp0\%PROJECT_FOLDER%"

:: === STEP 4: CREATE VENV ===
IF NOT EXIST .venv (
    echo [INFO] Creating virtual environment...
    %PYTHON_EXEC% -m venv .venv
    IF ERRORLEVEL 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: === STEP 5: INSTALL DEPENDENCIES ===
call .venv\Scripts\activate.bat
SET VENV_PY=.venv\Scripts\python.exe

IF NOT EXIST .venv\.setup_done (
    echo [INFO] Installing Python packages...
    %VENV_PY% -m pip install --upgrade pip
    %VENV_PY% -m pip install -r requirements.txt

    echo [INFO] Running Django migrations...
    %VENV_PY% manage.py migrate

    echo setup done > .venv\.setup_done
) ELSE (
    echo [INFO] Dependencies already installed.
)

:: === STEP 6: OPEN BROWSER ===
echo [INFO] Launching browser...
wscript launch_browser.vbs

ENDLOCAL
