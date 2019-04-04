#!/bin/bash

gunicorn --bind=0.0.0.0:8000 --log-level info --workers 4 twittor.wsgi:application