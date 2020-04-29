#!/bin/bash
uwsgi --http :5000 --wsgi-file wsgi.py --touch-reload wsgi.py
