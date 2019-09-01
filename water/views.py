# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json

from django.shortcuts import render

WATERFILE = '/home/pi/weather/results/water.json'

def get_season():
    now = datetime.datetime.now()
    d = now.timetuple().tm_yday
    if d <= 59:
        season = 'winter'
    elif 59 < d <= 151:
        season = 'spring'
    elif 151 < d <= 243:
        season = 'summer'
    elif 243 < d <= 334:
        season = 'fall'
    else:
        season = 'winter'
    return season


def water(request):

    try:
        with open(WATERFILE) as f:
            water = json.load(f)
        for dp in water['feeds']:
            dp['field1'] = round(((float(dp['field1'].split('\r')[0])*(9/5.))+32), 1)
            dp['created_at'] = datetime.datetime.strptime(dp['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        water = water['feeds'][::-1]
    except:
        water = [{'field1': 'n/a', 'created_at': 'n/a'}]

    context = {
        'season': get_season(),
        'page': 'Water Temperature',
        'water': water,
    }
    return render(request, 'water/water.html', context)
