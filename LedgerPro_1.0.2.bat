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
IF "%~1" NEQ "RESTARTED=1" (
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
        IF "%~1"=="RESTARTED=2" (
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



:: === STEP 2.5: CHECK / INSTALL POSTGRESQL ===

SET "PG_VERSION=17"
SET "PG_BASE=C:\Program Files\PostgreSQL\%PG_VERSION%"
SET "PG_BIN=%PG_BASE%\bin"
SET "PSQL_EXE="
SET "PG_INSTALLER=postgresql-installer.exe"
SET "PG_URL=https://get.enterprisedb.com/postgresql/postgresql-17.6-1-windows-x64.exe"



:: --------------------------------------------------
:: Check if PostgreSQL is already installed
:: --------------------------------------------------

where psql >nul 2>&1
IF NOT ERRORLEVEL 1 (
    for /f "delims=" %%P in ('where psql') do (
        SET "PSQL_EXE=%%P"
    )
)

IF NOT DEFINED PSQL_EXE (
    IF EXIST "%PG_BIN%\psql.exe" (
        SET "PSQL_EXE=%PG_BIN%\psql.exe"
        SET "PATH=%PATH%;%PG_BIN%"
    )
)




:: --------------------------------------------------
:: Install PostgreSQL if not found
:: --------------------------------------------------

IF NOT DEFINED PSQL_EXE (

    IF EXIST "%PG_INSTALLER%" (
        echo [INFO] Using existing PostgreSQL installer.
    ) ELSE (
        echo [INFO] Downloading PostgreSQL installer...
        curl.exe -L --fail --output "%PG_INSTALLER%" "%PG_URL%"

        IF ERRORLEVEL 1 (
            echo [ERROR] PostgreSQL download failed.
            pause
            exit /b 1
        )
    )

    echo.
    echo [INFO] Installing PostgreSQL...
    echo.

    start /wait "" "%PG_INSTALLER%" ^
        --mode unattended ^
        --unattendedmodeui none ^
        --superpassword postgres ^
        --servicename postgresql-x64-%PG_VERSION% ^
        --serverport 5432
)

:: --------------------------------------------------
:: Wait for PostgreSQL installation
:: --------------------------------------------------

IF NOT DEFINED PSQL_EXE (

    echo [INFO] Waiting for PostgreSQL installation...

    :WAIT_POSTGRES
    timeout /t 2 >nul

    IF EXIST "%PG_BIN%\psql.exe" (
        SET "PSQL_EXE=%PG_BIN%\psql.exe"
        SET "PATH=%PATH%;%PG_BIN%"
    ) ELSE (
        goto WAIT_POSTGRES
    )
)




:: --------------------------------------------------
:: Final verification
:: --------------------------------------------------

IF NOT DEFINED PSQL_EXE (
    echo [ERROR] PostgreSQL installation failed.
    pause
    exit /b 1
)

echo [INFO] PostgreSQL detected:
echo        %PSQL_EXE%


:: ==================================================
:: CREATE DATABASE AND USER
:: ==================================================

SET "PG_ADMIN_USER=postgres"
SET "PG_ADMIN_PASS=postgres"

SET "PG_USER=ledgerpro"
SET "PG_PASS=ledger123"
SET "PG_DB=ledgerpro"

echo.
echo ==========================================
echo Creating PostgreSQL Database...
echo ==========================================

SET "PGPASSWORD=%PG_ADMIN_PASS%"

:: --------------------------------------------------
:: Test PostgreSQL Connection
:: --------------------------------------------------

"%PG_BIN%\psql.exe" -U %PG_ADMIN_USER% -h localhost -p 5432 -d postgres -c "SELECT 1;" >nul 2>&1

IF ERRORLEVEL 1 (
    echo.
    echo [ERROR] Unable to connect to PostgreSQL.
    echo Check PostgreSQL superuser password.
    pause
    exit /b 1
)

:: --------------------------------------------------
:: Create User
:: --------------------------------------------------

"%PG_BIN%\psql.exe" -U %PG_ADMIN_USER% -h localhost -p 5432 -d postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='%PG_USER%';" | find "1" >nul

IF ERRORLEVEL 1 (

    echo [INFO] Creating PostgreSQL user...

    "%PG_BIN%\psql.exe" ^
        -U %PG_ADMIN_USER% ^
        -h localhost ^
        -p 5432 ^
        -d postgres ^
        -c "CREATE USER %PG_USER% WITH PASSWORD '%PG_PASS%';"

) ELSE (

    echo [INFO] User already exists.

)

:: --------------------------------------------------
:: Create Database
:: --------------------------------------------------

"%PG_BIN%\psql.exe" -U %PG_ADMIN_USER% -h localhost -p 5432 -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='%PG_DB%';" | find "1" >nul

IF ERRORLEVEL 1 (

    echo [INFO] Creating PostgreSQL database...

    "%PG_BIN%\createdb.exe" ^
        -U %PG_ADMIN_USER% ^
        -h localhost ^
        -p 5432 ^
        -O %PG_USER% ^
        %PG_DB%

) ELSE (

    echo [INFO] Database already exists.

)

:: --------------------------------------------------
:: Grant Privileges
:: --------------------------------------------------

echo [INFO] Granting privileges...

"%PG_BIN%\psql.exe" ^
    -U %PG_ADMIN_USER% ^
    -h localhost ^
    -p 5432 ^
    -d postgres ^
    -c "GRANT ALL PRIVILEGES ON DATABASE %PG_DB% TO %PG_USER%;"

SET "PGPASSWORD="

echo.
echo ==========================================
echo PostgreSQL Database Ready
echo ==========================================
echo Database : %PG_DB%
echo Username : %PG_USER%
echo Password : %PG_PASS%
echo.






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

:: ==================================================
:: CREATE db_config.json
:: ==================================================

IF EXIST "%~dp0\%PROJECT_FOLDER%" (

    echo.
    echo [INFO] Creating db_config.json...

    (
        echo {
        echo     "ENGINE": "django.db.backends.postgresql",
        echo     "NAME": "%PG_DB%",
        echo     "USER": "%PG_USER%",
        echo     "PASSWORD": "%PG_PASS%",
        echo     "HOST": "localhost",
        echo     "PORT": "5432",
        echo     "REMOTE_DATABASE_URL": "",
        echo     "CONN_MAX_AGE": 0,
        echo     "OPTIONS": {},
        echo     "ATOMIC_REQUESTS": false,
        echo     "TIME_ZONE": "Asia/Kolkata",
        echo     "CONN_HEALTH_CHECKS": false,
        echo     "AUTOCOMMIT": true
        echo }
    ) > "%~dp0\%PROJECT_FOLDER%\db_config.json"

    echo [INFO] db_config.json created successfully.

) ELSE (

    echo [WARNING] LedgerPro folder not found.
    echo db_config.json will be created after cloning.

)

:: ==================================================
:: END CREATE db_config.json
:: ==================================================

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

:: ==================================================
:: STEP 6: INSTALL & RUN LEDGERPRO DESKTOP APP
:: ==================================================

SET "APP_NAME=Ledger-Pro"
SET "APP_EXE=Ledger-Pro.exe"
SET "APP_URL=https://ledger.in.net/Ledger-Pro_Setup_1.0.1.exe"
SET "APP_INSTALLER=Ledger-Pro_Setup_1.0.1.exe"

echo.
echo ==========================================
echo Checking LedgerPro Desktop...
echo ==========================================

:: Check if application is already installed
SET "APP_FOUND="

IF EXIST "C:\Program Files\Ledger-Pro\%APP_EXE%" (
    SET "APP_FOUND=C:\Program Files\Ledger-Pro\%APP_EXE%"
)

IF NOT DEFINED APP_FOUND (
    IF EXIST "C:\Program Files (x86)\Ledger-Pro\%APP_EXE%" (
        SET "APP_FOUND=C:\Program Files (x86)\Ledger-Pro\%APP_EXE%"
    )
)

IF NOT DEFINED APP_FOUND (
    FOR /F "delims=" %%A IN ('where "%APP_EXE%" 2^>nul') DO (
        SET "APP_FOUND=%%A"
    )
)

:: --------------------------------------------------
:: Install if not found
:: --------------------------------------------------

IF NOT DEFINED APP_FOUND (

    echo [INFO] LedgerPro Desktop not found.
    echo [INFO] Downloading installer...

    curl.exe -L --fail -o "%APP_INSTALLER%" "%APP_URL%"

    IF ERRORLEVEL 1 (
        echo.
        echo [ERROR] Unable to download LedgerPro installer.
        pause
        exit /b 1
    )

    echo.
    echo [INFO] Installing LedgerPro Desktop...
    start /wait "" "%APP_INSTALLER%"

    del /f /q "%APP_INSTALLER%" >nul 2>&1

    :: Search again
    IF EXIST "C:\Program Files\Ledger-Pro\%APP_EXE%" (
        SET "APP_FOUND=C:\Program Files\Ledger-Pro\%APP_EXE%"
    )

    IF NOT DEFINED APP_FOUND (
        IF EXIST "C:\Program Files (x86)\Ledger-Pro\%APP_EXE%" (
            SET "APP_FOUND=C:\Program Files (x86)\Ledger-Pro\%APP_EXE%"
        )
    )

)

:: --------------------------------------------------
:: Run application
:: --------------------------------------------------

IF DEFINED APP_FOUND (

    echo.
    echo [INFO] Starting LedgerPro Desktop...
    start "" "%APP_FOUND%"

) ELSE (

    echo.
    echo [WARNING] LedgerPro Desktop installation completed,
    echo but executable could not be located.

)

echo.
echo ==========================================
echo Installation Completed Successfully.
echo ==========================================

ENDLOCAL
