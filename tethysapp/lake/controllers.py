from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import render_to_response
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button
from tethys_sdk.gizmos import TimeSeries, SelectInput
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from hs_restclient import HydroShare, HydroShareAuthBasic

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
import urllib.request
import urllib.error
import urllib.parse

LAKE_FILES = {
    "utah": ["awqms_utah.csv", "byu_utah.csv"],
    "deer": ["awqms_deer.csv", "byu_deer.csv"],
    "salt": ["awqms_salt.csv", "byu_salt.csv"]
}

lake_list = [('',''), ('Utah Lake', 'utah'), ('Great Salt Lake', 'salt'), ('Deer Creek Reservoir', 'deer')]

dataLake={}
values_awqms={}
values_byu={}

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
                              options=lake_list,
                              initial=['']
                              )
    select_data = SelectInput(display_text='Select Data',
                              name='select-data',
                              multiple=False,
                              options=[('',''), ('All', 'all'), ('AWQMS', 'awqms'), ('BYU', 'byu')],
                              initial=['']
                              )
    select_max = SelectInput(display_text='Select a Maximum Value',
                                 name='select-max',
                                 multiple=False,
                                 options=[('All', '0'), ('4 Standard Deviations', '4'), ('3 Standard Deviations', '3'), ('2 Standard Deviations', '2'), ('1 Standard Deviation', '1')],
                                 initial=[('All', '0')]
                                 )
    select_bdl = SelectInput(display_text='Select a Minimum Limit Value',
                             name='select-bdl',
                             multiple=False,
                             options=[('0', '0'), ('Reporting Limit', '1'), ('1/2 Reporting Limit', '0.5')],
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
    context['select_max'] = select_max
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
    lake_name = get_data.get('lake_name')
    lake_param = get_data.get('lake_param')

    context ={}
    context['fraction'] = fraction(lake_name,lake_param)
    return JsonResponse(context)

def fraction(lake_name, lake_param):
    dataLake = getFiles(lake_name).get('all')
    param = dataLake['Characteristic Name']==lake_param
    dataParam = dataLake[param]
    dp1 = dataParam['Sample Fraction'] == 'Dissolved'
    dp = dataParam[dp1]
    if len(dp) > 0:
        fraction_list = [('',''), ('Total', 'total'), ('Dissolved', 'dissolved')]
    else:
        fraction_list = [('','')]
    select_fraction = SelectInput(display_text='Select Fraction',
                              name='select-fraction',
                              multiple=False,
                              options=fraction_list,
                              initial=['']
                              )
    context=select_fraction
    return context

def lake_parameter(request):
    # to get the parameters of the lake
    get_data = request.GET
    lake_name = get_data.get('lake_name')
    lake_data = get_data.get('lake_data')
    dataLake = getFiles(lake_name).get(lake_data)
    #read all the chlorophyll a as one parameter called Chlorophyll a
        #chl = {'Chlorophyll a, uncorrected for pheophytin':'Chlorophyll a','Chlorophyll a, corrected for pheophytin':'Chlorophyll a','Chlorophyll a, free of pheophytin':'Chlorophyll a'}
        #dataLake = dataLake.replace(chl)
    parameter_list1 = dataLake['Characteristic Name'].unique().tolist()
    parameter_list1.sort()
    parameter_list1.insert(0, ' ')
    parameter_list = list(zip(*([parameter_list1] + [parameter_list1])))
    select_parameter = SelectInput(display_text='Select Parameter',
                              name='select-parameter',
                              multiple=False,
                              options=parameter_list,
                              initial=['']
                              )
    context ={}
    context['parameter'] = select_parameter
    return JsonResponse(context)

@login_required()
def charact_data(request):
    get_data = request.GET
    lake_name = get_data.get('lake_name')
    lake_data = get_data.get('lake_data')
    lake_param = get_data.get('lake_param')
    param_max = get_data.get('param_max')
    param_fract = get_data.get('param_fract')
    param_bdl = get_data.get('param_bdl')

    context = {}
    context = getData(lake_name, lake_data, lake_param, param_fract, param_max, param_bdl)
    print(context['csvGraph']['Result Value'].head(20))
    return JsonResponse(context)

def getFiles(lake_name):

    # Obtener archivos y separarlos segun lago y organizacion(o los dos juntos)
    awqms=LAKE_FILES.get(lake_name)[0]
    byu=LAKE_FILES.get(lake_name)[1]

    #using hydroshare files
    url1 = 'https://www.hydroshare.org/resource/cf0133c4d4a14a7f938918707abb4e05/data/contents/{0}'.format(awqms)
    file_path = requests.get(url1, verify=False).content
    url2 = 'https://www.hydroshare.org/resource/cf0133c4d4a14a7f938918707abb4e05/data/contents/{0}'.format(byu)
    file_path_byu = requests.get(url2, verify=False).content
    dataLake_awqms = pd.read_csv(io.StringIO(file_path.decode('utf-8')))
    dataLake_byu = pd.read_csv(io.StringIO(file_path_byu.decode('utf-8')))

    #using app files
    # app_workspace = app.get_app_workspace()
    # file_path = os.path.join(app_workspace.path, LAKE_FILES.get(lake_name)[0])
    # file_path_byu = os.path.join(app_workspace.path, LAKE_FILES.get(lake_name)[1])
    # dataLake_awqms = pd.read_csv(file_path, encoding= 'unicode_escape')
    # dataLake_byu = pd.read_csv(file_path_byu, encoding= 'unicode_escape')

    dataLake_byu['Organization ID'] = 'BYU'
    fields = ['Activity Start Date', 'Organization ID', 'Monitoring Location ID', 'Monitoring Location Name', 'Monitoring Location Latitude', 'Monitoring Location Longitude',
              'Monitoring Location Type', 'Characteristic Name', 'Sample Fraction', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']

    values_awqms = dataLake_awqms[fields]
    values_byu = dataLake_byu[fields]
    dataLake_all = [values_awqms, values_byu]
    dataLake = pd.concat(dataLake_all, ignore_index=True)
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
    #chl = {'Chlorophyll a, uncorrected for pheophytin':'Chlorophyll a','Chlorophyll a, corrected for pheophytin':'Chlorophyll a','Chlorophyll a, free of pheophytin':'Chlorophyll a'}
    #dataLake = dataLake.replace(chl)
    param = dataLake['Characteristic Name'] == lake_param
    row_param = dataLake[param]
    #row_param['Result Value']=row_param['Result Value'].astype('float64')

        # check Total-Dissolved
    if param_fract == 'Dissolved' or param_fract == 'Total':
        fract = row_param['Sample Fraction'] == param_fract
        row_all = row_param[fract]
    else:
        row_all = row_param
    #row_param.to_csv('row_param.csv', index=False, encoding='utf-8')

        # Add values to the No Detected, acording the selected bdl
    context = {}
    context['csvParameter'] = row_all
    #print(context['csvParameter']['Result Value'].head(20))
    x=float(param_bdl)
    avoid_changes = row_all['Characteristic Name'] == lake_param
    row_min = row_all[avoid_changes]
    row_min['Result Value'] = row_min['Result Value'].astype('float64')
    row_min['Result Value'].fillna(row_min['Detection Limit Value1']*x, inplace=True)
    stan_dev = np.std(row_min['Result Value'])
    mean = np.mean(row_min['Result Value'])
    if param_max != '0':
        m=float(param_max)
        sd=float(stan_dev)
        y=mean+(sd*m)
        print (y)
        maxim = row_min['Result Value'] <= y
        row = row_min[maxim]
    else:
        row = row_min

    locations = row['Monitoring Location ID'].unique()
    unit = row['Result Unit'].unique()
    unit = ''.join(unit)
    context['characteristic'] = lake_param
    context['fraction'] = param_fract
    context['unit'] = unit
    #context['csvLake'] = dataLake
    context['csvGraph'] = row
    print(context['csvGraph']['Result Value'].head(20))
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

    # Completar el time series para los graficos
    df['Date'] = pd.to_datetime(df['Activity Start Date'])

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
