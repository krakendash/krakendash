from django.conf.urls import patterns, include, url

base_urlpatterns = patterns(
    '',
    url(r'^$', 'status.views.home', name='home'),
    url(r'^ops/$', 'ops.views.ops', name='ops'),
    url(r'^osd/(\d+)/$', 'status.views.osd_details', name='osd_details'),
    url(r'^activity/$', 'status.views.activity', name='activity'),
    url(r'^user/(.+?)(/.+?)?(/.+?)?/$', 'ops.views.user_custom',
        name='user_custom'),
    url(r'^api/$', "status.views.api", name="api"),
)

urlpatterns = patterns('',
    url(r'krakendash/', include(base_urlpatterns)),
)
