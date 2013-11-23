# coding: utf-8
import json
from django.core.urlresolvers import reverse
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
            q_filters |= Q(iata_code__icontains=filter_str)
            q_filters |= Q(icao_code__icontains=filter_str)
    return filters, q_filters


class Paging(object):
    def __init__(self, data_query, path, page, func_of_view=None, page_col=10):
        data_count = data_query.count()
        self.act_page = page
        path = path.replace('page={0}'.format(page), 'page={0}')
        page_c = page * page_col
        self.count_page = data_count/page_col+1 if float(data_count)/page_col > data_count/page_col else data_count/page_col
        self.data_list = data_query[page_c-page_col:page_c]
        self.pages = self.get_pages_list(page, self.count_page, path)
        if func_of_view:
            for data in self.data_list:
                data.link = reverse(func_of_view, kwargs={'pk': data.pk, 'page': '1', 'filter': ''})

        self.next_page = path.format(page + 1)
        self.prev_page = path.format(page - 1)
        self.first_page = path.format(1)
        self.last_page = path.format(self.count_page)
        super(Paging, self).__init__()

    def get_pages_list(self, page, page_count, path):
        active = lambda x: 'active' if x == page else ''
        pages = range(page_count+1)
        if page < 3:
            pages = pages[1:6]
        elif page_count-page < 3:
            if page_count > 5:
                pages = pages[-5:]
            else:
                pages = pages[1:]
        else:
            pages = pages[page-2:page+3]
        result = [{'status': active(pag), 'number': pag, 'link': path.format(pag)} for pag in pages]
        return result