@echo off
setlocal enabledelayedexpansion

REM Read the backup folder path from backup_path.txt
set "CONFIG_FILE=%~dp0backup_path.txt"
if not exist "%CONFIG_FILE%" (
    echo ❌ Config file not found: %CONFIG_FILE%
    exit /b 1
)

for /f "usebackq delims=" %%a in ("%CONFIG_FILE%") do set "BACKUP_FOLDER=%%a"

REM Go to the backup folder
pushd "%BACKUP_FOLDER%"

REM Zip all .sql files and delete them after zipping
for %%f in (*.sql) do (
    echo 🔄 Zipping %%f...
    powershell Compress-Archive -Path "%%f" -DestinationPath "%%~nf.zip" -Force
    if exist "%%~nf.zip" (
        del "%%f"
        echo 🗑️ Deleted %%f after compression
    )
)

popd
