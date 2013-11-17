# coding: utf-8
import json
from django.http import HttpResponse
from django.template import loader, Context
from airports_catalog.airports.models import Country, City, Airport


def return_airports(request, *args, **kwargs):
    template = loader.get_template('index.html')
    context = Context()
    return HttpResponse(template.render(context), 'text/html')


def return_countries_json(request):
    countries = Country.objects.all().order_by('eng_name')
    countries_dict = [{'iso': obj.iso_code, 'eng_name': obj.eng_name} for obj in countries]

    return HttpResponse(json.JSONEncoder().encode(countries_dict), content_type="application/json")


def return_cities_json(request):
    cities = City.objects.all().order_by('eng_name')[:1000]
    cities_dict = [{'id': obj.id, 'eng_name': obj.eng_name} for obj in cities]

    return HttpResponse(json.JSONEncoder().encode(cities_dict), content_type="application/json")


def return_airports_json(request):
    airports = Airport.objects.all().order_by('eng_name')
    airports_dict = [{'iata': obj.iata_code, 'eng_name': obj.eng_name} for obj in airports]

    return HttpResponse(json.JSONEncoder().encode(airports_dict), content_type="application/json")
