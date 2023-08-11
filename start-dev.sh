#!/bin/sh



echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo "Starting server"
python manage.py runserver 0.0.0.0:8000
