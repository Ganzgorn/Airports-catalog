from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from airports_catalog.airports.views import return_airports_json, return_cities_json, return_countries_json

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'airports_catalog.airports.views.return_airports'),
    url(r'^countries$', return_countries_json),
    url(r'^cities$', return_cities_json),
    url(r'^airports$', return_airports_json),

    # Examples:
    #url(r'^$', 'airports_catalog.views.return_airports', name='home'),
    # url(r'^airports_catalog/', include('airports_catalog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
