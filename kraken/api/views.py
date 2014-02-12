from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.conf import settings
from cephclient import wrapper
import json

"""
API Endpoint that grabs the cluster data
"""
#get_data = wrapper.CephWrapper(endpoint=settings.CEPH_BASE_URL)

get_data = wrapper.CephWrapper(endpoint=settings.CEPH_BASE_URL)

"""
Master API view that has all sublinks
"""
@api_view(['GET'])
def api(request, format=None):
	return Response({"clusters-url": reverse("clusters", request=request),
					"health-url": reverse("cluster-health", request=request),
					"status-url": reverse("cluster-status", request=request)})

"""
Master clusters view that just has hyperlinks to the subviews for now
"""
@api_view(['GET'])
def clusters(request, format=None):
	return Response({"health-url": reverse("cluster-health", request=request),
					"status-url": reverse("cluster-status", request=request)})

"""
Get Health data about the cluster
"""
@api_view(['GET'])
def health(request, format=None):
	health_response, cluster_health = get_data.health(body='json')
	return Response(cluster_health)

"""
Get Status data about the cluster
"""
@api_view(['GET'])
def status(request, format=None):
	status_response, cluster_status = get_data.status(body='json')
	return Response(cluster_status)