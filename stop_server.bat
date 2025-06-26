@echo off
echo [INFO] Checking for processes using port 8000...

FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') DO (
    echo [INFO] Killing process ID %%P using port 8000
    taskkill /PID %%P /F >nul 2>&1
)

echo [INFO] All processes on port 8000 have been terminated.
pause
