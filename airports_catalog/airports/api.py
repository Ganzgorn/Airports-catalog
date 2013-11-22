# coding: utf-8
import json
from django.db.models import Q
from airports_catalog.airports.models import Country, City, Airport
MODELS_DICT = {
    'Country': Country,
    'City': City,
    'Airport': Airport,
}


def get_data_from_model(model, filters=None):
    model = MODELS_DICT.get(model)
    assert model
    if filters[1]:
        result = model.objects.filter(filters[1])
    else:
        result = model.objects.filter(**filters[0])
    result = result.order_by('eng_name').values_list('pk', 'eng_name')
    return result


def get_filters(request, model):
    q_filters = None
    filters = json.JSONDecoder().decode(request.GET.get('filter', '{}'))
    for mod in filters.keys():
        assert mod.lower() in [i.lower() for i in MODELS_DICT.keys()]
    if 'query_filter' in request.GET:
        filter_str = request.GET['query_filter']
        q_filters = Q(
            Q(eng_name__icontains=filter_str) |
            Q(rus_name__icontains=filter_str)
        )
        if model =='Country':
            q_filters |= Q(iso_code__icontains=filter_str)
        elif model == 'Airport':
            q_filters |= Q(iata_code=filter_str)
            q_filters |= Q(icao_code=filter_str)
    return filters, q_filters


def get_pages_list(page, page_count, path):
    active = lambda x: 'active' if x == page else ''
    pages = range(page_count+1)
    if page < 3:
        pages = pages[1:6]
    elif page_count-page < 3:
        pages = pages[-5:]
    else:
        pages = pages[page-2:page+3]
    result = [{'status': active(pag), 'number': pag, 'link': path.format(pag)} for pag in pages]
    return result