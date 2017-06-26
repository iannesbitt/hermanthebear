# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.shortcuts import render

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


def snow(request):

    context = {
        'season': get_season(),
        'page': 'Snow Depth',
    }
    return render(request, 'snow/snow.html', context)
