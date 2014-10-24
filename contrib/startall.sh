#!/bin/bash
screen -dmS api ceph-rest-api -c /etc/ceph/ceph.conf --cluster ceph -i admin
python /app/manage.py runserver  0.0.0.0:8000
