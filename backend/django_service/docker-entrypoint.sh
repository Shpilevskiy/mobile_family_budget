#!/bin/bash
# wait for PostgreSQl server to start
sleep 10
su -m apiuser -c "gunicorn -b :8000 -w 4  mobile_family_budget.wsgi:application --reload"