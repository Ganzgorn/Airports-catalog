# coding: utf-8
import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from airports_catalog.airports.api import MODELS_DICT, get_filters, get_data_from_model, Paging
from airports_catalog.airports.models import Country, City, Airport
from django.core.urlresolvers import reverse


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
    q_filters = Q(
        Q(eng_name__icontains=filter_str) |
        Q(rus_name__icontains=filter_str) |
        Q(iso_code__icontains=filter_str)
    ) if filter_str else Q()

    countries = Country.objects.filter(q_filters).order_by('iso_code')
    paging = Paging(countries, request.path, int(kwargs.get('page', 1)), get_list_of_city)

    context = {
        'countries': paging.data_list,
        'paging': paging
    }
    return render_to_response('countries_list.html', context)


def get_list_of_city(request, **kwargs):
    pk = kwargs.get('pk')
    slug = kwargs.get('slug')
    filter_str = kwargs.get('filter')
    q_filters = Q(
        Q(eng_name__icontains=filter_str) |
        Q(rus_name__icontains=filter_str)
    ) if filter_str else Q()

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

    cities = City.objects.filter(country=country).filter(q_filters).order_by('eng_name')
    paging = Paging(cities, request.path, int(kwargs.get('page', 1)), get_list_of_airports)

    context = {
        'country': country.display(),
        'cities': paging.data_list,
        'change_country': reverse(get_list_of_country, kwargs={'page': 1, 'filter': ''}),
        'paging': paging

    }
    return render_to_response('cities_list.html', context)


def get_list_of_airports(request, **kwargs):
    pk = kwargs.get('pk')
    slug = kwargs.get('slug')
    filter_str = kwargs.get('filter')
    q_filters = Q(
        Q(eng_name__icontains=filter_str) |
        Q(rus_name__icontains=filter_str) |
        Q(iata_code__icontains=filter_str) |
        Q(icao_code__icontains=filter_str)
    ) if filter_str else Q()

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

    airports = Airport.objects.filter(city=city).filter(q_filters).order_by('iata_code')
    paging = Paging(airports, request.path, int(kwargs.get('page', 1)))

    for airport in paging.data_list:
        airport.link = reverse(get_airport, kwargs={'pk': airport.pk})
    context = {
        'country': city.country.display(),
        'city': city.display(),
        'airports': paging.data_list,
        'change_country': reverse(get_list_of_country, kwargs={'page': 1, 'filter': ''}),
        'change_city': reverse(get_list_of_city, kwargs={'pk': city.country.pk, 'page': 1, 'filter': ''}),
        'paging': paging
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