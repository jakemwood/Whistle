#!/bin/sh
python manage.py migrate
cd frontend
yarn install && yarn build
cd ..
python manage.py collectstatic

