from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    #url(r'^$', 'airports_catalog.airports.views'),
    # Examples:
    # url(r'^$', 'airports_catalog.views.home', name='home'),
    # url(r'^airports_catalog/', include('airports_catalog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
