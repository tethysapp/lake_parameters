from django.shortcuts import render
from django.shortcuts import reverse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button
from tethys_sdk.gizmos import TimeSeries, SelectInput
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta

from csv import writer as csv_writer
import plotly.graph_objs as go
import requests
import numpy as np
import pandas as pd
import io
import json
import os
import math
from .app import Lake as app
from pandas import DataFrame
from .utils import download

LAKE_FILES = {
    "utah": ["awqms_utah.csv", "byu_utah.csv"],
    "salt": ["awqms_salt.csv", "byu_salt.csv"]
}

PARAM_MAX = {
    "Chlorophyll a": [('Unlimited', '0')],
    'Dissolved oxygen (DO)': [('Unlimited', '0')],
    'Phosphate-phosphorus': [('Unlimited', '0'), ('5', '5'), ('2', '2'), ('1', '1')],
    'Nitrogen': [('Unlimited', '0'), ('10', '10'), ('5', '5'), ('2', '2')],
    'Magnesium': [('Unlimited', '0'), ('5', '5'), ('2', '2'), ('1', '1')],
    'Orthophosphate': [('',''), ('Unlimited', '0'), ('5', '5'), ('2', '2'), ('1', '1')],
    'pH': [('Unlimited', '0')],
    'Temperature, water': [('Unlimited', '0')],
    'Turbidity': [('Unlimited', '0')],
    'Depth, Secchi disk depth': [('Unlimited', '0')],
    'Total dissolved solids': [('Unlimited', '0')]
}

@login_required()
def home(request):
    context = {
    }
    return render(request, 'lake/home.html', context)

@login_required()
def data(request):
    select_lake = SelectInput(display_text='Select a Lake',
                              name='select-lake',
                              multiple=False,
                              options=[('Utah Lake', 'utah'), ('Salt Lake', 'salt')],
                              initial=['Utah Lake']
                              )
    select_data = SelectInput(display_text='Select Data',
                              name='select-data',
                              multiple=False,
                              options=[('All', 'all'), ('AWQMS', 'awqms'), ('BYU', 'byu')],
                              initial=['']
                              )
    select_parameter = SelectInput(display_text='Select a Parameter',
                                   name='select-parameter',
                                   multiple=False,
                                   options=[('',''), ('Chlorophyll-a', 'Chlorophyll a'), ('Dissolved Oxygen', 'Dissolved oxygen (DO)'), ('Phosphate-phosphorus', 'Phosphate-phosphorus'), ('Nitrogen', 'Nitrogen'), ('Magnesium', 'Magnesium'), ('Orthophosphate', 'Orthophosphate'), ('pH', 'pH'), ('Water Temperature', 'Temperature, water'), ('Turbidity', 'Turbidity'), ('Secchi Disk Depth', 'Depth, Secchi disk depth'), ('Total Dissolved Solids', 'Total dissolved solids')],
                                   initial=['']
                                   )
    select_bdl = SelectInput(display_text='Select a value for Data below Detection Limit',
                             name='select-bdl',
                             multiple=False,
                             options=[('0', '0'), ('Detection Limit', '1'), ('1/2 Detection Limit', '0.5')],
                             initial=[('0', '0')]
                             )

    getstations = getStations('utah')
    context = {}
    context['all_coords_stations'] = getstations['all_coords_stations']
    context['dif_coords_stations'] = getstations['dif_coords_stations']
    context['all_stations'] = getstations['all_stations']
    context['lake_map'] = getstations['lake_map']
    context['select_lake'] = select_lake
    context['select_data'] = select_data
    context['select_parameter'] = select_parameter

    context['select_bdl'] = select_bdl

    return render(request, 'lake/data.html', context)

@login_required()
def instructions(request):
    context = {
    }
    return render(request, 'lake/instructions.html', context)

@login_required()
def get_lake(request):
    get_data = request.GET
    lake_name = get_data.get('lake_name')
    context = getStations(lake_name)
    return JsonResponse(context)

@login_required()
def param_fraction(request):
    # to get the fraction and the maximum
    get_data = request.GET
    lake_param = get_data.get('lake_param')
    context ={}
    context['fraction'] = fraction(lake_param)
    context['maximum'] = maximum(lake_param)
    print(context)
    return JsonResponse(context)

def fraction(lake_param):
    if lake_param =='Phosphate-phosphorus' or lake_param =='Nitrogen' or lake_param =='Magnesium':
        fraction_list = [('',''), ('Total', 'total'), ('Dissolved', 'dissolved')]
    else:
        fraction_list = [('','')]
    select_fraction = SelectInput(display_text='Select Fraction (only for some parameters)',
                              name='select-fraction',
                              multiple=False,
                              options=fraction_list,
                              initial=['']
                              )
    context=select_fraction
    return context

def maximum(lake_param):
    if lake_param =='Phosphate-phosphorus' or lake_param =='Nitrogen' or lake_param =='Magnesium':
        fraction_list = [('',''), ('Total', 'total'), ('Dissolved', 'dissolved')]
    else:
        fraction_list = [('','')]
    select_max = SelectInput(display_text='Select a maximum value',
                             name='select-max',
                             multiple=False,
                             options=PARAM_MAX.get(lake_param),
                             initial=['']
                             )
    context=select_max
    return context

@login_required()
def charact_data(request):
    get_data = request.GET
    lake_name = get_data.get('lake_name')
    lake_data = get_data.get('lake_data')
    lake_param = get_data.get('lake_param')
    param_max = get_data.get('param_max')
    param_fract = get_data.get('param_fract')
    param_bdl = get_data.get('param_bdl')
    print (lake_name)
    # context = {}
    context = getData(lake_name, lake_data, lake_param, param_fract, param_max, param_bdl)
    # print(context)
    # download_button = download()
    # context['download_button'] = download_button
    # return render(request, 'lake/show_data.html', context)
    return JsonResponse(context)

def getFiles(lake_name):

    # Obtener archivos y separarlos segun lago y organizacion(o los dos juntos)
    # print(selectlake)
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, LAKE_FILES.get(lake_name)[0])
    file_path_byu = os.path.join(app_workspace.path, LAKE_FILES.get(lake_name)[1])

    dataLake_awqms = pd.read_csv(file_path)
    dataLake_byu = pd.read_csv(file_path_byu)
    dataLake_byu['Organization ID'] = 'BYU'

    fields = ['Activity Start Date', 'Organization ID', 'Monitoring Location ID', 'Monitoring Location Name', 'Monitoring Location Latitude', 'Monitoring Location Longitude',
              'Monitoring Location Type', 'Characteristic Name', 'Sample Fraction', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']

    values_awqms = dataLake_awqms[fields]
    values_byu = dataLake_byu[fields]
    dataLake_all = [values_awqms, values_byu]
    dataLake = pd.concat(dataLake_all, ignore_index=True)
    # print(dataLake)
    context = {
        'all': dataLake,
        'awqms': values_awqms,
        'byu': values_byu
    }

    return context

def getStations(lake_name):

    # Obtner estaciones segun lago para el mapa de estaciones

    dataLake = getFiles(lake_name).get('all')
    locations = dataLake['Monitoring Location ID'].unique()
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
            in_out_lake = df['Monitoring Location Type'].tolist()[0]
            station = df['Monitoring Location Name'].tolist()[0]
            dataname = str(location)
            context['all_stations'][dataname] = {'coords': [lat, lon], 'org': organization, 'type': in_out_lake,'station': station}
    lats = dataLake['Monitoring Location Latitude'].unique()
    lons = dataLake['Monitoring Location Longitude'].unique()
    lats_mean = (np.max(lats)+np.min(lats))/2
    lons_mean = (np.max(lons)+np.min(lons))/2
    lats_dif = np.max(lats)-np.min(lats)
    lons_dif = np.max(lons)-np.min(lons)
    context['all_coords_stations'] = [lats_mean, lons_mean]
    context['dif_coords_stations'] = [lats_dif, lons_dif]
    return context

def getData(lake_name, lake_data, lake_param, param_fract, param_max, param_bdl):
    # Obtener datos segun el parametro y su fraccion, mandar datos con el timeseries completo
    dataLakeAll = getFiles(lake_name).get('all')
    dataLake = getFiles(lake_name).get(lake_data)
    chl = {'Chlorophyll a, uncorrected for pheophytin':'Chlorophyll a','Chlorophyll a, corrected for pheophytin':'Chlorophyll a','Chlorophyll a, free of pheophytin':'Chlorophyll a'}
    dataLake = dataLake.replace(chl)
    param = dataLake['Characteristic Name'] == lake_param
    row_param = dataLake[param]
    # print(row_param)

        # check Total-Dissolved
    if param_fract == 'Dissolved' or param_fract == 'Total':
        fract = row_param['Sample Fraction'] == param_fract
        row_all = row_param[fract]
    else:
        row_all = row_param

        # erase below maximum
    if param_max != 'Unlimited' and param_max != '':
        m = float(param_max)
        maxim = row_all['Result Value']<m
        row = row_all[maxim]
    else:
        row = row_all

        # Add values to the No Detected, acording the selected bdl
    x=float(param_bdl)
    row['DeLiVal']=row['Detection Limit Value1']*x
    row['Result Value'].fillna(row['DeLiVal'], inplace=True)

    locations = row['Monitoring Location ID'].unique()
    unit = row['Result Unit'].unique()
    unit = ''.join(unit)
    context = {}
    context['characteristic'] = lake_param
    #context['fraction'] = fraction
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
            in_out_lake = df['Monitoring Location Type'].tolist()[0]
            station = df['Monitoring Location Name'].tolist()[0]
            dataname = str(location)
            charac_id = row['Monitoring Location ID'] == location
            charac = row[charac_id]
            responseObject = {}
            valuesFin, alldates = completeSeries(charac)
            responseObject['values'] = valuesFin
            responseObject['dates'] = alldates
            # print(responseObject)
            context['all_data'][dataname] = {'coords': [lat, lon], 'org': organization, 'type': in_out_lake, 'station': station, 'data': responseObject}
    lats = dataLakeAll['Monitoring Location Latitude'].unique()
    lons = dataLakeAll['Monitoring Location Longitude'].unique()
    lats_mean = (np.max(lats)+np.min(lats))/2
    lons_mean = (np.max(lons)+np.min(lons))/2
    lats_dif = np.max(lats)-np.min(lats)
    lons_dif = np.max(lons)-np.min(lons)
    context['all_coords_stations'] = [lats_mean, lons_mean]
    context['dif_coords_stations'] = [lats_dif, lons_dif]
    return context

def completeSeries(df):
    # print(df)
    # Completar el time series para los graficos
    df['Date'] = pd.to_datetime(df['Activity Start Date'])

    # df = df.sort_values(by=['Date'])
    #
    # dateslist = df['Date'].tolist()
    # inidate = dateslist[0]
    # findate = dateslist[-1]
    # alldates = []
    # curdate = inidate
    # while curdate <= findate:
    #     alldates.append(curdate)
    #     curdate = curdate + timedelta(days=1)
    #
    # df2 = pd.DataFrame(alldates, columns=['Date'])
    #
    # dfjoin = df2.merge(df, on='Date', how='left')
    # value = dfjoin['Result Value']
    # dates = dfjoin['Date']

    value = df['Result Value']
    dates = df['Date']

    datesString = []
    valuesNumpy = value.to_numpy(value)
    valuesNoNan = np.nan_to_num(valuesNumpy, nan=-999)
    valuesFin = valuesNoNan.tolist()
    for datesX in dates:
        datesString.append(str(datesX).split()[0])
    alldates = datesString
    return valuesFin, alldates
