python manage.py migrate
gunicorn gymnash.wsgi:application --workers 2 --bind 0.0.0.0:9000