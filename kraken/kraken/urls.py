from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from api import views

#viewsets define the view behavior.
#router = routers.DefaultRouter()
#router.register(r'clusters', views.ClusterViewSet, 'cluster')

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^$', 'status.views.home', name='home'),
    url(r'^ops/$', 'status.views.ops', name='ops'),
    url(r'^osd/(\d+)/$', 'status.views.osd_details', name='osd_details'),
    url(r'^api/clusters/health/$', views.health, name="cluster-health"),
    url(r'^api/clusters/status/$', views.status, name="cluster-status"),
    url(r'^api/clusters/$', views.clusters, name="clusters"),
    url(r'^api/$', views.api, name="api"),
)
