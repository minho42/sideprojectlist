release: python manage.py migrate
web: gunicorn sideprojectlist.wsgi
celeryworker: celery -A sideprojectlist worker -l info -O fair
