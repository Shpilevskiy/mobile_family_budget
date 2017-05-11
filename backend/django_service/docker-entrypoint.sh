#!/bin/bash
# wait for PostgreSQl server to start
sleep 10

echo "from django.contrib.auth.models import User; User.objects.create_superuser('adminadmin', 'admin@example.com', 'adminadmin')" | python manage.py shell
su -m apiuser -c "gunicorn -b :8000 -w 4  mobile_family_budget.wsgi:application --reload"