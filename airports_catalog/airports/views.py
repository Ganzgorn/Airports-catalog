# coding: utf-8
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from airports_catalog.airports.api import MODELS_DICT, get_filters, get_data_from_model, get_pages_list
from airports_catalog.airports.models import Country, City, Airport
from django.core.urlresolvers import resolve, reverse


def return_select_mode(request):
    context = {'link_urls_mode': reverse(get_list_of_country, kwargs={'page': 1, 'filter': ''})}
    return render_to_response('index.html', context)


def return_airports(request):
    return render_to_response('dynamic_catalog.html')


def return_data_json(request):
    if 'model' in request.GET:
        model = request.GET['model']
    else:
        return HttpResponse(json.JSONEncoder().encode([]), content_type="application/json")
    filters = get_filters(request, model)

    objects = get_data_from_model(model, filters)
    result_dict = [{'id': obj[0], 'eng_name': obj[1]} for obj in objects]
    return HttpResponse(json.JSONEncoder().encode(result_dict), content_type="application/json")


def get_data_row(request):
    args = request.GET

    if 'model' in args:
        model = MODELS_DICT.get(request.GET['model'], [])
        obj = model.objects.get(pk=args['id'])

    result_dict = vars(obj)
    result_dict.pop('_state')
    result_dict['type_location'] = obj.get_type_location_display()
    return HttpResponse(json.JSONEncoder().encode(result_dict), content_type="application/json")


def get_list_of_country(request, **kwargs):
    filter_str = kwargs.get('filter')
    page_actual = int(kwargs.get('page', 1))
    path = request.path.replace('page={0}'.format(page_actual), 'page={0}')
    page_col = 10
    page_c = page_actual * page_col

    countries = Country.objects.filter().order_by('iso_code')
    countries_count = countries.count()
    countries = countries[page_c-page_col:page_c]

    page_count = countries_count/page_col+1 if float(countries_count)/page_col > countries_count/page_col else countries_count/page_col
    pages = get_pages_list(page_actual, page_count, path)
    for country in countries:
        country.link = reverse(get_list_of_city, kwargs={'pk': country.pk, 'page': '1', 'filter': ''})

    context = {
        'countries': countries,
        'paging': {
            'count_page': page_count,
            'pages': pages,
            'act_page': page_actual,
            'next_page': path.format(page_actual + 1),
            'prev_page': path.format(page_actual - 1),
            'first_page': path.format(1),
            'last_page': path.format(page_count),
        }
    }
    return render_to_response('countries_list.html', context)


def get_list_of_city(request, **kwargs):
    pk = kwargs.get('pk')
    slug = kwargs.get('slug')
    filter_str = kwargs.get('filter')
    page_actual = int(kwargs.get('page', 1))
    path = request.path.replace('page={0}'.format(page_actual), 'page={0}')
    page_col = 10
    page_c = page_actual * page_col

    if pk:
        try:
            country = Country.objects.get(iso_code=pk)
        except Country.DoesNotExist:
            return get_list_of_country #TODO: Выводить ошибку
    elif slug:
        try:
            country = Country.objects.get(slug=slug)
        except Country.DoesNotExist:
            return get_list_of_country #TODO: Выводить ошибку
    else:
        return get_list_of_country #TODO: Выводить ошибку

    cities = City.objects.filter(country=country).order_by('eng_name')
    cities_count = cities.count()
    cities = cities[page_c-page_col:page_c]

    page_count = cities_count/page_col+1 if float(cities_count)/page_col > cities_count/page_col else cities_count/page_col
    pages = get_pages_list(page_actual, page_count, path)
    for city in cities:
        city.link = reverse(get_list_of_airports, kwargs={'pk': city.pk, 'page': '1', 'filter': ''})

    context = {
        'country': country.display(),
        'cities': cities,
        'change_country': reverse(get_list_of_country, kwargs={'page': 1, 'filter': ''}),
        'paging': {
            'count_page': page_count,
            'pages': pages,
            'act_page': page_actual,
            'next_page': path.format(page_actual + 1),
            'prev_page': path.format(page_actual - 1),
            'first_page': path.format(1),
            'last_page': path.format(page_count),
        }
    }
    return render_to_response('cities_list.html', context)


def get_list_of_airports(request, **kwargs):
    pk = kwargs.get('pk')
    slug = kwargs.get('slug')
    filter_str = kwargs.get('filter')
    page_actual = int(kwargs.get('page', 1))
    path = request.path.replace('page={0}'.format(page_actual), 'page={0}')
    page_col = 10
    page_c = page_actual * page_col

    if pk:
        try:
            city = City.objects.get(id=pk)
        except City.DoesNotExist:
            return get_list_of_country #TODO: Выводить ошибку
    elif slug:
        try:
            city = City.objects.get(slug=slug)
        except City.DoesNotExist:
            return get_list_of_country #TODO: Выводить ошибку
    else:
        return get_list_of_country #TODO: Выводить ошибку

    airports = Airport.objects.filter(city=city).order_by('iata_code')
    airports_count = airports.count()
    airports = airports[page_c-page_col:page_c]

    page_count = airports_count/page_col+1 if float(airports_count)/page_col > airports_count/page_col else airports_count/page_col
    pages = get_pages_list(page_actual, page_count, path)

    for airport in airports:
        airport.link = reverse(get_airport, kwargs={'pk': airport.pk})
    context = {
        'country': city.country.display(),
        'city': city.display(),
        'airports': airports,
        'change_country': reverse(get_list_of_country, kwargs={'page': 1, 'filter': ''}),
        'change_city': reverse(get_list_of_city, kwargs={'pk': city.country.pk, 'page': 1, 'filter': ''}),
        'paging': {
            'count_page': page_count,
            'pages': pages,
            'act_page': page_actual,
            'next_page': path.format(page_actual + 1),
            'prev_page': path.format(page_actual - 1),
            'first_page': path.format(1),
            'last_page': path.format(page_count),
        }
    }
    return render_to_response('airports_list.html', context)


def get_airport(request, **kwargs):
    pk = kwargs.get('pk')
    slug = kwargs.get('slug')

    if pk:
        try:
            airport = Airport.objects.get(iata_code=pk)
        except Airport.DoesNotExist:
            return get_list_of_country #TODO: Выводить ошибку
    elif slug:
        try:
            airport = Airport.objects.get(slug=slug)
        except Airport.DoesNotExist:
            return get_list_of_country #TODO: Выводить ошибку
    else:
        return get_list_of_country #TODO: Выводить ошибку

    return render_to_response('airport.html', {
        'country': airport.city.country.display(),
        'city': airport.city.display(),
        'airport': airport.display(),
        'change_country': reverse(get_list_of_country, kwargs={'page': 1, 'filter': ''}),
        'change_city': reverse(get_list_of_city, kwargs={'pk': airport.city.country.pk, 'page': 1, 'filter': ''}),
        'change_airport': reverse(get_list_of_airports, kwargs={'pk': airport.city.pk, 'page': 1, 'filter': ''})
    })