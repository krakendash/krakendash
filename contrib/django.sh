#!/usr/bin/env bash
python krakendash/manage.py runserver 0.0.0.0:8000 > kraken.log 2>&1 &
