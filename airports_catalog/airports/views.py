# coding: utf-8
import json
from django.http import HttpResponse
from django.template import loader, Context
from airports_catalog.airports.api import get_countries, MODELS_DICT, get_filters


def return_airports(request):
    template = loader.get_template('index.html')
    context = Context()
    return HttpResponse(template.render(context), 'text/html')


def return_data_json(request):
    if 'model' in request.GET:
        model = request.GET['model']
    else:
        return HttpResponse(json.JSONEncoder().encode([]), content_type="application/json")
    filters = get_filters(request, model)

    objects = get_countries(model, filters)
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

