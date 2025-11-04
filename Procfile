release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn craynew.wsgi:application --bind 0.0.0.0:$PORT
