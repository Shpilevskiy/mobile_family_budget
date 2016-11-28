#!/bin/bash
su -m apiuser -c "gunicorn -w 2 mobile_family_budget.wsgi"