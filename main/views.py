# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
import datetime
import pytz
from pywws import conversions
import pandas as pd

from django.shortcuts import render

CONDITIONSNOW = '/home/pi/weather/results/json_latest.txt'
CONDITIONSNOWBKP = '/home/pi/weather/results/json_latest_bkp.txt'
CONDITIONSHR = '/home/pi/weather/results/json_hour.txt'
CONDITIONSHRBKP = '/home/pi/weather/results/json_hour_bkp.txt'
HEATERFILE = '/home/pi/weather/results/heater.txt'
WATERFILE = '/home/pi/weather/results/water.json'
SNOWDEPTH = '/home/pi/weather/results/snowdepth'
DEPTH_CALIB=1736.

def snowdepth(day):
    file = os.path.join(SNOWDEPTH, day.strftime('%Y-%m-%d') + '.csv')
    depthfile = os.path.join(SNOWDEPTH, 'snow.txt')
    depthfile24h = os.path.join(SNOWDEPTH, '24hsnow.txt')

    with open(file, 'r') as f:
        time, mm = f.readlines()[-1].split(',')
        time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    with open(depthfile, 'r') as f:
        mm = float(f.read().rstrip())
    with open(depthfile24h, 'r') as f:
        mm24h = float(f.read().rstrip())

    return time, mm, mm24h

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

def mod_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def index(request):
    try:
        try:
            with open(CONDITIONSNOW) as f:
                data1 = json.load(f)
        except:
            with open(CONDITIONSNOWBKP) as f:
                data1 = json.load(f)

        try:
            with open(CONDITIONSHR) as f:
                data0 = json.load(f)
        except:
            with open(CONDITIONSHRBKP) as f:
                data0 = json.load(f)

        data0[0]['TempOut'] = round(conversions.temp_f(data0[0]['TempOut']), 1)
        data1[0]['TempOut'] = round(conversions.temp_f(data1[0]['TempOut']), 1)

        data0[0]['FeelsLike'] = round(conversions.temp_f(data0[0]['FeelsLike']), 1)
        data1[0]['FeelsLike'] = round(conversions.temp_f(data1[0]['FeelsLike']), 1)

        data0[0]['AbsPressure'] = conversions.pressure_inhg(data0[0]['AbsPressure'] + 281)
        data1[0]['AbsPressure'] = conversions.pressure_inhg(data1[0]['AbsPressure'] + 281)
        deltapress = round(data1[0]['AbsPressure']-data0[0]['AbsPressure'], 3)
        data1[0]['AbsPressure'] = round(data1[0]['AbsPressure'], 3)

        data1[0]['WindAvg'] = round(conversions.wind_mph(data1[0]['WindAvg']), 1)
        data1[0]['WindGust'] = round(conversions.wind_mph(data1[0]['WindGust']), 1)

        data1[0]['Rain'] = round(conversions.rain_inch(data1[0]['Rain']), 2)

    except:
        pass

    try:
        deltatemp = round(data1[0]['TempOut']-data0[0]['TempOut'], 2)
        deltahum = data1[0]['HumidityOut']-data0[0]['HumidityOut']
    except:
        deltatemp = 'n/a'
        deltahum = 'n/a'

    if float(deltatemp) > 0.0:
        deltatemp = str('+' + str(deltatemp))
    if float(deltahum) > 0.0:
        deltahum = str('+' + str(deltahum))
    if float(deltapress) > 0.0:
        deltapress = str('+' + str(deltapress))

    now = datetime.datetime.now()
    mod = now-mod_date(HEATERFILE)

    with open(HEATERFILE) as f:
        heater = f.read()
        if str(heater) == 'OFF\n':
            clr = '00d'
        else:
            clr = 'c00'

    with open(WATERFILE) as f:
        water = json.load(f)

    deltadir = ''

    try:
        last_depth = snowdepth(now)
        depth = last_depth[1]
        deltadepth = depth - last_depth[2]
        depthmod = now - last_depth[0]
        depth = round(depth, 1)
        deltadepth = round(deltadepth, 1)
        depthmod = round(depthmod.total_seconds()/60., 1)
        if deltadepth > 0.:
            deltadir = '+'
    except:
        depth = 'n/a'
        depthmod = ''
        deltadepth = 'n/a'

    context = {
        'data': data1[0],
        'deltatemp': deltatemp,
        'deltahum': deltahum,
        'deltapress': deltapress,
        'deltatime': data0[0]['Time'],
        'heater': heater,
        'watertemp': water['temperature'],
        'heatermod': round(mod.total_seconds()/60, 1),
        'depth': depth,
        'deltadepth': deltadepth,
        'deltadir': deltadir,
        'depthmod': depthmod,
        'clr': clr,
        'season': get_season(),
        'page': 'Bear Weather Report',
    }
    return render(request, 'main/index.html', context)

def webcam(request):

    context = {
        'clar': datetime.datetime.now().strftime('%Y%m%d'),
        'season': get_season(),
        'page': 'Webcam',
    }
    return render(request, 'main/webcam.html', context)

def about(request):

    context = {
        'season': get_season(),
        'page': 'About',
    }
    return render(request, 'main/about.html', context)

def history(request):

    context = {
        'season': get_season(),
        'page': 'Weather History',
    }
    return render(request, 'main/history.html', context)

#def snow(request):
#    context = {
#        'season': get_season(),
#        'page': 'Weather History',
#    }
