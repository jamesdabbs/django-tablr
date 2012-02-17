from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tablr.views',
    url(r'^(?P<id>[a-z0-9]+)/$', 'render_qa', name='render_qa'), 
    url(r'^$', 'home'),
)
