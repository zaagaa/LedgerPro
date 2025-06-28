@echo off
setlocal enabledelayedexpansion

REM Set log file path
set "LOGFILE=%~dp0log.txt"
echo. >> "%LOGFILE%"
echo [%DATE% %TIME%] 🔄 Script started >> "%LOGFILE%"

REM Path to config.py
set "CONFIG_FILE=%~dp0config.py"

if not exist "%CONFIG_FILE%" (
    echo ❌ Config file not found: %CONFIG_FILE%
    echo [%DATE% %TIME%] ❌ Config file not found: %CONFIG_FILE% >> "%LOGFILE%"
    pause
    exit /b 1
)

echo 📄 Reading BACKUP_DIR from: %CONFIG_FILE%
echo [%DATE% %TIME%] 📄 Reading BACKUP_DIR from: %CONFIG_FILE% >> "%LOGFILE%"

REM Extract BACKUP_DIR from config.py using PowerShell and save to temp file
set "TEMP_BACKUP_FILE=%TEMP%\backup_dir_path.txt"
powershell -nologo -command ^
    "Get-Content -Path '%CONFIG_FILE%' | ForEach-Object { if ($_ -match 'BACKUP_DIR\s*=\s*r?[\"''](.+)[\"'']') { $matches[1] } }" > "%TEMP_BACKUP_FILE%"

REM Read extracted path from temp file
set /p BACKUP_FOLDER=<"%TEMP_BACKUP_FILE%"
del "%TEMP_BACKUP_FILE%" >nul 2>&1

echo DEBUG: BACKUP_FOLDER = !BACKUP_FOLDER!
echo [%DATE% %TIME%] 🐞 DEBUG BACKUP_FOLDER = !BACKUP_FOLDER! >> "%LOGFILE%"

if not defined BACKUP_FOLDER (
    echo ❌ Could not extract BACKUP_DIR from config.py
    echo [%DATE% %TIME%] ❌ Could not extract BACKUP_DIR from config.py >> "%LOGFILE%"
    pause
    exit /b 1
)

if not exist "!BACKUP_FOLDER!\" (
    echo ❌ Folder does not exist: !BACKUP_FOLDER!
    echo [%DATE% %TIME%] ❌ Backup folder does not exist: !BACKUP_FOLDER! >> "%LOGFILE%"
    pause
    exit /b 1
)

echo 📁 BACKUP_FOLDER set to: "!BACKUP_FOLDER!"
echo [%DATE% %TIME%] 📁 BACKUP_FOLDER: !BACKUP_FOLDER! >> "%LOGFILE%"

REM Navigate to the backup folder
pushd "!BACKUP_FOLDER!"
echo [%DATE% %TIME%] 📂 Entered backup folder: !BACKUP_FOLDER! >> "%LOGFILE%"

REM Zip .sql files
set "FILES_FOUND=false"
for %%f in (*.sql) do (
    set "FILES_FOUND=true"
    echo 🔄 Zipping %%f...
    echo [%DATE% %TIME%] 🔄 Zipping %%f >> "%LOGFILE%"
    powershell -nologo -command "Compress-Archive -Path '%%f' -DestinationPath '%%~nf.zip' -Force"
    if exist "%%~nf.zip" (
        del "%%f"
        echo 🗑️ Deleted %%f after compression
        echo [%DATE% %TIME%] 🗑️ Deleted %%f >> "%LOGFILE%"
    ) else (
        echo ⚠️ Compression failed for %%f
        echo [%DATE% %TIME%] ⚠️ Compression failed for %%f >> "%LOGFILE%"
    )
)

if not !FILES_FOUND! == true (
    echo ℹ️ No .sql files found in backup folder
    echo [%DATE% %TIME%] ℹ️ No .sql files found in backup folder >> "%LOGFILE%"
)

REM Return to original folder
popd
echo [%DATE% %TIME%] 🔚 Finished processing >> "%LOGFILE%"

echo  Done
pause
