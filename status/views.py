# Copyright (c) 2013,2014 Donald Talton
# All rights reserved.

# Redistribution and use in source and binary forms,
# with or without modification,
# are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.

# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# Neither the name of Donald Talton nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import re

from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.conf import settings
from cephclient import wrapper
from humanize import suffixes
from rgwadmin import RGWAdmin, exceptions


def home(request):
    """
    Main dashboard, Overall cluster health and status
    """

    response = {}

    ceph = wrapper.CephWrapper(endpoint=settings.CEPH_BASE_URL)

    cresp, response['cluster_health'] = ceph.health(body='json')
    sresp, cluster_status = ceph.status(body='json')

    # Monitors
    all_mons = cluster_status['output']['monmap']['mons']
    up_mons = (cluster_status['output']['health']['health']
                             ['health_services'][0]['mons'])
    total_mon_count = len(all_mons)
    response['mons'] = {'ok': 0, 'warn': 0, 'crit': 0}

    for mon in up_mons:
        if mon['health'] == "HEALTH_OK":
            response['mons']['ok'] += 1
        else:
            response['mons']['warn'] += 1

    response['mons']['crit'] = total_mon_count - (
        response['mons']['ok'] + response['mons']['crit']
    )

    # Get a rough estimate of cluster free space. Is this accurate ?
    bytes_total = cluster_status['output']['pgmap']['bytes_total']
    bytes_used = cluster_status['output']['pgmap']['bytes_used']

    def filesize(value):
        value = float(value)
        if value == 1:
            return '1 Byte'
        elif value < 1024 ** 2:
            return '%d Bytes' % value
        for i, s in enumerate(suffixes['decimal']):
            unit = 1024 ** (i + 2)
            if value < unit * 1024:
                return i, (1024 * value / unit), s
        return i, (1024 * value / unit), s

    (response['scale'],
     response['data_avail'],
     response['data_scale']) = filesize(bytes_total)
    response['data_used'] = round(float(bytes_used)/(1024.0 ** (response['scale'] + 1)), 1)
    # pgs
    pg_statuses = cluster_status['output']['pgmap']

    response['pg'] = {'ok': 0, 'warn': 0, 'crit': 0}
    # pg states
    pg_warn_status = re.compile("(creating|degraded|replay|splitting|"
                                "scrubbing|repair|recovering|backfill"
                                "|wait-backfill|remapped)")
    pg_crit_status = re.compile("(down|inconsistent|incomplete|stale|peering)")

    for state in pg_statuses['pgs_by_state']:
        if state['state_name'] == "active+clean":
            response['pg']['ok'] += state['count']

        elif pg_warn_status.search(state['state_name']):
            response['pg']['warn'] += state['count']

        elif pg_crit_status.search(state['state_name']):
            response['pg']['crit'] += state['count']

    # pg statuses
    response['pg']['stat'] = dict()

    for state in pg_statuses['pgs_by_state']:
        response['pg']['stat'][state['state_name']] = state['count']

    # osds
    dresp, osd_dump = ceph.osd_dump(body='json')
    response['osd'] = {'state': osd_dump['output']['osds'],
                       'ok': 0, 'warn': 0, 'crit': 0}

    for osd_status in response['osd']['state']:
        if osd_status["in"] and osd_status["up"]:
            response['osd']['ok'] += 1
        elif osd_status["in"] == 0 and osd_status["up"] == 0:
            response['osd']['crit'] += 1
        else:
            response['osd']['warn'] += 1

    # Users and stats
    s3_servers = list(settings.S3_SERVERS)
    response['users'] = {'stat': get_users_stat(s3_servers)}
    
    # RGW statuses
    response['radosgw'] = {'stat': dict(), 'ok': 0, 'fail': 0}

    for server in settings.S3_SERVERS:
        stat = get_rgw_stat(server)
        response['radosgw']['stat'][server] = stat
        if stat:
            response['radosgw']['ok'] += 1
        else:
            response['radosgw']['fail'] += 1

    if 'json' in request.GET:
        return JsonResponse(response)
    else:
        return render_to_response('dashboard.html', response)


def get_rgw_stat(server):
    try:
        rgwAdmin = RGWAdmin(settings.S3_ACCESS, settings.S3_SECRET,
                            server, secure=False)
        if rgwAdmin.get_users():
            return 1
        else:
            return 0
    except:
        return 0

def get_users_stat(s3_servers):
    users_stat = {}
    try:
        rgwAdmin = RGWAdmin(settings.S3_ACCESS, settings.S3_SECRET,
                            s3_servers.pop(0), secure=False) 
        buckets_list = rgwAdmin.get_bucket()
        for bucket in buckets_list:
            try:
                bucket_stat = rgwAdmin.get_bucket(bucket)
                if bucket_stat["owner"] in users_stat:
                    if "rgw.main" in bucket_stat["usage"]:
                        users_stat[
                            bucket_stat["owner"]
                        ][bucket] = bucket_stat["usage"]["rgw.main"]
                    else:
                        users_stat[
                            bucket_stat["owner"]
                        ][bucket] = {}
                else:
                    if "rgw.main" in bucket_stat["usage"]:
                        users_stat[bucket_stat["owner"]] = {
                            bucket: bucket_stat["usage"]["rgw.main"]}
                    else:
                        users_stat[bucket_stat["owner"]] = {
                            bucket: {}}
            except:
                pass
        return users_stat
    except IndexError:
        return users_stat
    except TypeError:
        return get_users_stat(s3_servers)
    except exceptions.ServerDown:
        return get_users_stat(s3_servers)


def osd_details(request, osd_num):
    ceph = wrapper.CephWrapper(endpoint=settings.CEPH_BASE_URL)
    osd_num = int(osd_num)

    reponse, osd_dump = ceph.osd_dump(body='json')
    osd_disk_details = filter(
        lambda x: x['osd'] == int(osd_num), osd_dump['output']['osds']
    )[0]
    import socket
    osd_disk_details["name"] = socket.gethostbyaddr(
        osd_disk_details["public_addr"].split(":")[0]
    )[0].split(".")[0]

    response, osd_perf = ceph.osd_perf(body='json')
    osd_disk_perf = filter(lambda x: x['id'] == int(osd_num),
                           osd_perf['output']['osd_perf_infos'])[0]

    return render_to_response('osd_details.html',
                              {'osd_disk': {'details': osd_disk_details,
                                            'perf': osd_disk_perf}})


def activity(_):
    ceph = wrapper.CephWrapper(endpoint=settings.CEPH_BASE_URL)

    sresp, cluster_status = ceph.status(body='json')
    pgmap = cluster_status['output']['pgmap']
    activities = {}
    if 'read_bytes_sec' in pgmap:
        activities['Read'] = pgmap.get('read_bytes_sec')
    if 'write_bytes_sec' in pgmap:
        activities['Write'] = pgmap.get('write_bytes_sec')
    if 'op_per_sec' in pgmap:
        activities['Ops'] = pgmap.get('op_per_sec')
    if 'recovering_objects_per_sec' in pgmap:
        activities['Recovering_Objects'] = pgmap.get(
            'recovering_objects_per_sec')
    if 'recovering_bytes_per_sec' in pgmap:
        activities['Recovery_Speed'] = pgmap.get('recovering_bytes_per_sec')
    if 'recovering_keys_per_sec' in pgmap:
        activities['Recovering_Keys'] = pgmap.get('recovering_keys_per_sec')
    
    # Free size
    bytes_total = pgmap.get('bytes_total')
    bytes_used = pgmap.get('bytes_used')
    
    activities['Used'] = bytes_used
    activities['Total'] = bytes_total

    return JsonResponse(activities)


def api(_):
    return render_to_response("api.html")
