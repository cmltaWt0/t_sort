__author__ = 'dixon'

from django.http import JsonResponse
import json
from datetime import datetime, timedelta


def index(request):
    data = request.GET.get('json')
    if data is None or not data:
        return JsonResponse({'error': 'json data is not specified'})
    try:
        data = json.loads(data)
    except (ValueError, TypeError) as e:
        return JsonResponse({"error": e})

    if not isinstance(data, dict) or not "toSort" in data:
        return JsonResponse({'error': 'Wrong json data'})

    to_sort = data["toSort"]

    d_values = [datetime.strptime(i['d'], "%d:%m:%Y") for i in to_sort]
    p_values = [i['p'] for i in to_sort]
    r_values = [i['r'] for i in to_sort]

    d_range = (min(d_values), max(d_values))
    p_range = (min(p_values), max(p_values))
    r_range = (min(r_values), max(r_values))

    d_step = (d_range[1] - d_range[0]).days / 10.0
    p_step = (p_range[1] - p_range[0]) / 10.0
    r_step = (r_range[1] - r_range[0]) / 10.0

    def normalize(v, min_v, s):
        if isinstance(min_v, datetime):
            v = datetime.strptime(v, "%d:%m:%Y")
        d = v - min_v
        if isinstance(d, timedelta):
            d = d.days
        return d / s - 5

    for item in to_sort:
        norm_d = normalize(item['d'], d_range[0], d_step)
        norm_p = normalize(item['p'], p_range[0], p_step)
        norm_r = normalize(item['r'], r_range[0], r_step)
        item['weight'] = norm_d * data['dPriority'] + norm_p * data['pPriority'] + norm_r * data['rPriority']

    sorted_list = sorted(to_sort, key=lambda i: i['weight'])
    response = JsonResponse(sorted_list, safe=False)

    if 'callback' in request.GET:
        callback = request.GET['callback']

        response.content = "%s(%s)" % (callback, response.content)

    return response