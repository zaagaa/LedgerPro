@echo off
cd /d %~dp0

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate

echo [INFO] Running migrations...
python manage.py migrate

echo [INFO] Starting Django development server...
python manage.py runserver 0.0.0.0:8000
