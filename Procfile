web: bash -c "echo '🔥 Starting Gunicorn...' && python manage.py migrate && gunicorn BusinessApp.wsgi:application --bind 0.0.0.0:$PORT --log-level debug --log-file -"
