from django.shortcuts import render
from django.shortcuts import reverse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button
from tethys_sdk.gizmos import TimeSeries
from django.http import HttpResponse, JsonResponse
from datetime import datetime

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
import glob


@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    dataJson = dataLake.to_dict()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'jsonLake':dataJson
    }

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
        'lake_map': lake_map,
    }
    return render(request, 'lake/add_data.html', context)

@login_required()
def instructions(request):
    """
    Controller for the Instructions page.
    """

    context = {
    }

    return render(request, 'lake/instructions.html', context)


def getData(characteristic):
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    # file_path = os.path.join(app_workspace.path, "awqms_lake.xlsx")

    # file_path_miller = os.path.join(app_workspace.path, "Miller_data.xlsx")
    # dataLake_awqms = pd.read_excel(file_path)
    # dataLake_miller = pd.read_excel(file_path_miller)
    file_path_miller = os.path.join(app_workspace.path, "Miller_data.csv")
    dataLake_awqms = pd.read_csv(file_path)
    dataLake_miller = pd.read_csv(file_path_miller)
    values_awqms = dataLake_awqms[['Activity Start Date', 'Monitoring Location ID', 'Monitoring Location Name', 'Characteristic Name', 'Sample Fraction', 'Monitoring Location Latitude', 'Monitoring Location Longitude', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']]
    values_miller = dataLake_miller[['Activity Start Date', 'Monitoring Location ID', 'Monitoring Location Name', 'Characteristic Name', 'Sample Fraction', 'Monitoring Location Latitude', 'Monitoring Location Longitude', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']]
    dataLake_all = [values_awqms, values_miller]
    dataLake = pd.concat(dataLake_all)

    param = dataLake['Characteristic Name'] == characteristic
    row = dataLake[param]
    locations = row['Monitoring Location ID'].unique()
    unit = row['Result Unit'].unique()
    print(unit)
    locations.sort()
    context = {}
    context['characteristic'] = characteristic
    context['unit'] = unit
    # context['csvLake'] = dataLake
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
            dataname = str(location)
            charac_id = row['Monitoring Location ID'] == location
            charac = row[charac_id]
            value = charac['Result Value']
            print(value)
            date = charac['Activity Start Date']
            # date.index = pd.to_datetime(date.index)

            valuesNumpy = value.to_numpy()
            # convierte los vacios en ceros
            valuesNoNan = np.nan_to_num(valuesNumpy)
            valuesFin = valuesNoNan.tolist()
            # print(valuesNoNan)
            # sacar el 1
            responseObject = {}
            responseObject['values'] = valuesFin
            responseObject['dates'] = date.to_numpy().tolist()
            #
            # print(responseObject)
            # borrar
            # date1 = responseObject1['dates'][0]
            # date_len = len(responseObject1['dates'])
            # date2 = responseObject1['dates'][date_len - 1]
            # start = datetime.datetime(date1)
            # end = datetime.datetime(date2)
            # date_complete = pd.date_range(start, end)
            # print(responseObject1['dates'])
            # print(date_complete)
            # responseObject = {}
            # responseObject['dates'] = date_complete
            # responseObject['values'] = responseObject1['values']
            # print(responseObject)
            # print(responseObject1['values'])
            #

            context['all_data'][dataname] = {'coords': [lat, lon], 'data': responseObject}
    return context



def chl_a(request):
    context = getData('Chlorophyll a, uncorrected for pheophytin')
    #print(context)
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
