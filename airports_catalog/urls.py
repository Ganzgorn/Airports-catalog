from django.conf.urls import patterns, include, url
from django.contrib import admin
from airports_catalog.airports.views import return_data_json, get_data_row, get_list_of_country

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'airports_catalog.airports.views.return_select_mode'),
    url(r'^ajax_mode$', 'airports_catalog.airports.views.return_airports'),
    url(r'^countries', get_list_of_country),
    url(r'^get_rows', return_data_json),
    url(r'^get_row', get_data_row),

    url(r'^admin/', include(admin.site.urls)),
)
