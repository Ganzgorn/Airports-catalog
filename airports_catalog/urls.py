from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import resolve, reverse
p_f = '/page=(?P<page>\d+)/filter=(?P<filter>[A-Za-z0-9-]*)' # Page + filter
admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^$', 'airports_catalog.airports.views.return_select_mode'),
    url(r'^ajax_mode$', 'airports_catalog.airports.views.return_airports'),
    url(r'^countries' + p_f, 'airports_catalog.airports.views.get_list_of_country'),
    url(r'^country/(?P<slug>\d{1}-[A-Z]{2}-[A-Za-z0-9-]+)' + p_f, 'airports_catalog.airports.views.get_list_of_country'),
    url(r'^country/(?P<pk>[A-Z]{2})' + p_f, 'airports_catalog.airports.views.get_list_of_city'),
    url(r'^city/(?P<slug>\d{1}-[0-9-]+-[0-9-]+-[A-Za-z0-9-]+)' + p_f, 'airports_catalog.airports.views.get_list_of_airports'),
    url(r'^city/(?P<pk>\d+)' + p_f, 'airports_catalog.airports.views.get_list_of_airports'),
    url(r'^airport/(?P<slug>\d{1}-[A-Z]{3}-[A-Za-z0-9-]+)', 'airports_catalog.airports.views.get_airport'),
    url(r'^airport/(?P<pk>[A-Z]{3})', 'airports_catalog.airports.views.get_airport'),
    url(r'^get_rows', 'airports_catalog.airports.views.return_data_json'),
    url(r'^get_row', 'airports_catalog.airports.views.get_data_row'),

    url(r'^admin/', include(admin.site.urls)),
)
