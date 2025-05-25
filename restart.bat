@echo off
timeout /t 1 >nul
start cmd /k "python manage.py runserver"
exit
