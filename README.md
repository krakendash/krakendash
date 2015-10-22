# kraken + S3

A free Ceph dashboard for stats and monitoring

Come hang out with us on freenode in #kraken-dashboard

## Overview

![Status dashboard](/screenshots/status.png?raw=true "Status")

![User panel](/screenshots/users.png?raw=true "Users")

![User mod](/screenshots/user_mod.png?raw=true "User mod")

## Installation and Roadmap

### Prerequisites:

Python 2.7

The ceph-rest-api must be run on either a member of your Ceph cluster, or on a installed client node that has admin access to the cluster.


### Ubuntu Installation:

```
  sudo su -
  apt-get update && apt-get install -y python-pip python-dev libxml2-dev libxslt-dev
  git clone https://github.com/krakendash/krakendash.git
  cp krakendash/contrib/*.sh .
  cd krakendash
  pip install -r requirements.txt
```

In /root you now have two scripts: 

api.sh starts the ceph-rest-api in a screen session called api
django.sh starts krakendash in a screen session called django

To reattach to a session, use:
```
  screen -ls
```
This gives a list of your sessions. The session name will appears as $PID.{api|django}, re-attach using:
```
  screen -r $NAME
```


Now you can run Kraken!

./api.sh (if you are running kraken on a ceph client or cluster node)
./django.sh

### Systemd-based system

```
  sudo su -
  yum upgrade && yum install -y python-pip python-devel libxml2-devel libxslt-devel
  cd /var/www
  git clone https://github.com/krakendash/krakendash.git
  cp krakendash/contrib/systemd/* /etc/systemd/system/multi-user.target.wants/
  systemctl daemon-reload
  cd krakendash
  pip install -r requirements.txt
  systemctl start ceph-rest-api krakendash
```  
  
If you are not running Kraken on a Ceph node, edit krakendash/kraken/settings.py. Here you can change CEPH_BASE_URL to point at your host running ceph-rest-api. Copy the api.sh script to that host and run it as root. Kraken will then talk to that API endpoint for cluster data.

## Milestone One
- [x] Cluster status
- [x] Cluster data usage
- [x] MON status
- [x] OSD status
- [x] PG status
- [x] Better UI
- [x] Multi-MON support
- [x] Migrate from requests to [python-cephclient](https://github.com/dmsimard/python-cephclient/)

## Milestone Two
- [] MON operations
- [] OSD operations
- [] Pool operations
- [] List pools, size
- [] Pool status
- [] View CRUSH map

### Milestone Three
- [] Auth system
- [] User session tracking

### Milestone Four
- [] Collectd integration
- [] Graphite integration
- [] Multi-cluster support

### Milestone S3 One
- [x] S3 users stats
- [x] S3 users administration
- [x] S3 users customize and quotes
