from django.shortcuts import render
from django.shortcuts import reverse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button
from tethys_sdk.gizmos import TimeSeries
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from csv import writer as csv_writer
import plotly.graph_objs as go
import requests
import numpy as np
import pandas as pd
import io
import os
import math
from .app import Lake as app
from pandas import DataFrame


@login_required()
def home(request):
    context = getStations()
    return render(request, 'lake/home.html', context)

@login_required()
def add_data(request):
    """
    Controller for the Search Data page.
    """
    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map
            }
    return render(request, 'lake/add_data.html', context)

@login_required()
def instructions(request):
    context = {
    }

    return render(request, 'lake/instructions.html', context)

def getFiles():
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    file_path_miller = os.path.join(app_workspace.path, "Miller_data.csv")
    dataLake_awqms = pd.read_csv(file_path)
    dataLake_miller = pd.read_csv(file_path_miller)
    dataLake_miller['Organization ID'] = 'BYU, Dr Miller'
    # print(dataLake_miller['Organization ID'])
    values_awqms = dataLake_awqms[['Organization ID', 'Monitoring Location ID', 'Monitoring Location Name', 'Characteristic Name', 'Monitoring Location Latitude', 'Monitoring Location Longitude', 'Activity Start Date', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']]
    values_miller = dataLake_miller[['Organization ID', 'Monitoring Location ID', 'Monitoring Location Name', 'Characteristic Name', 'Monitoring Location Latitude', 'Monitoring Location Longitude', 'Activity Start Date', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']]
    dataLake_all = [values_awqms, values_miller]
    dataLake = pd.concat(dataLake_all)
    context = dataLake
    return context

def getStations():
    dataLake = getFiles()
    locations = dataLake['Monitoring Location ID'].unique()
    # locations.sort()
    # print(locations)
    context = {}

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )
    context['lake_map'] = lake_map
    context['all_stations'] = {}

    for location in locations:
        df = dataLake[dataLake['Monitoring Location ID'] == location]
        if len(df) > 0:
            lat = df['Monitoring Location Latitude'].tolist()[0]
            lon = df['Monitoring Location Longitude'].tolist()[0]
            organization = df['Organization ID'].tolist()[0]
            station = df['Monitoring Location Name'].tolist()[0]
            dataname = str(location)
            context['all_stations'][dataname] = {'coords': [lat, lon], 'org': organization, 'station': station}
    return context

def completeSeries(df):
    df['Date'] = pd.to_datetime(df['Activity Start Date'], format = "%m-%d-%Y")
    df = df.sort_values(by = ['Date'])
    dateslist = df['Date'].tolist()
    inidate = dateslist[0]
    findate = dateslist[-1]
    alldates = []
    curdate = inidate
    while curdate <= findate:
        alldates.append(curdate)
        curdate = curdate + timedelta(days = 1)
    df2 = pd.DataFrame(alldates, columns = ['Date'])
    dfjoin = df2.merge(df, on = 'Date', how = 'left')
    value = dfjoin['Result Value']
    dates = dfjoin['Date']
    valuesNumpy = value.to_numpy()
    valuesNoNan = np.nan_to_num(valuesNumpy)
    valuesFin = valuesNoNan.tolist()
    alldates = dates.to_numpy().tolist()
    return valuesFin, alldates

def getData(characteristic):
    dataLake = getFiles()
    param = dataLake['Characteristic Name'] == characteristic
    row = dataLake[param]
    # print(row)
    locations = row['Monitoring Location ID'].unique()
    unit = row['Result Unit'].unique()
    # locations.sort()
    # print(locations)
    context = {}
    context['characteristic'] = characteristic
    context['unit'] = unit
    context['csvLake'] = dataLake

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )
    context['lake_map'] = lake_map
    context['all_data'] = {}

    for location in locations:
        df = dataLake[dataLake['Monitoring Location ID'] == location]
        if len(df) > 0:
            lat = df['Monitoring Location Latitude'].tolist()[0]
            lon = df['Monitoring Location Longitude'].tolist()[0]
            organization = df['Organization ID'].tolist()[0]
            dataname = str(location)
            charac_id = row['Monitoring Location ID'] == location
            charac = row[charac_id]
            responseObject = {}
            valuesFin, alldates = completeSeries(charac)
            responseObject['values'] = valuesFin
            responseObject['dates'] = alldates
            context['all_data'][dataname] = {'coords': [lat, lon], 'org': organization, 'data': responseObject}
    return context

def chl_a(request):
    context = getData('Chlorophyll a, uncorrected for pheophytin')
    return render(request, 'lake/show_data.html', context)

def do(request):
    context = getData('Dissolved oxygen (DO)')
    return render(request, 'lake/show_data.html', context)

def magn(request):
    context = getData('Magnesium')
    return render(request, 'lake/show_data.html', context)

def nit(request):
    context = getData('Nitrogen')
    return render(request, 'lake/show_data.html', context)

def ph(request):
    context = getData('pH')
    return render(request, 'lake/show_data.html', context)

def phosp(request):
    context = getData('Phosphate-phosphorus')
    return render(request, 'lake/show_data.html', context)

def water_temp(request):
    context = getData('Temperature, water')
    return render(request, 'lake/show_data.html', context)

def tds(request):
    context = getData('Total dissolved solids')
    return render(request, 'lake/show_data.html', context)

def turb(request):
    context = getData('Turbidity')
    return render(request, 'lake/show_data.html', context)

def secchi(request):
    context = getData('Depth, Secchi disk depth')
    return render(request, 'lake/show_data.html', context)

def ortho(request):
    context = getData('Ortho Phosphorus')
    return render(request, 'lake/show_data.html', context)

def precip(request):
    context = getData('Precipitation')
    return render(request, 'lake/show_data.html', context)
