release: python manage.py migrate --no-input && python manage.py collectstatic --no-input
web: gunicorn config.wsgi:application
