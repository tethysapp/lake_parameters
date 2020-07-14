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
import os
import math
from .app import Lake as app
from pandas import DataFrame
from .utils import download
# from .utils import get_select_lake, get_select_parameter, get_select_bdl, get_select_data, get_select_max

LAKE_FILES = {
    "utah": ["awqms_utah.csv", "byu_utah.csv"],
    "salt": ["awqms_salt.csv", "byu_salt.csv"]
}


@login_required()
def home(request):
    select_lake = SelectInput(display_text='Select a Lake',
                              name='select-lake',
                              multiple=False,
                              options=[('Utah Lake', 'utah'), ('Salt Lake', 'salt')],
                              initial=['Utah Lake']
                              )
    select_data = SelectInput(display_text='Select Data',
                              name='select-data',
                              multiple=False,
                              options=[('All', '1'), ('AWQMS', '2'), ('BYU', '3')],
                              initial=['All']
                              )
    select_parameter = SelectInput(display_text='Select a Parameter',
                                   name='select-parameter',
                                   multiple=False,
                                   options=[('Chlorophyll-a', '1'), ('Dissolved Oxygen', '2'), ('Phosphate-phosphorus', '3'), ('Nitrogen', '4'), ('Magnesium', '5'), ('Ortho Phosphorus',
                                                                                                                                                                      '6'), ('pH', '7'), ('Water Temperature', '8'), ('Turbidity', '9'), ('Secchi Disk Depth', '10'), ('Total Dissolved Solids', '11')],
                                   initial=['Chlorophyll-a']
                                   )
    select_bdl = SelectInput(display_text='Select a value for Data below Detection Limit',
                             name='select-bdl',
                             multiple=False,
                             options=[('0', '1'), ('Detection Limit', '2'), ('1/2 Detection Limit', '3')],
                             initial=['0']
                             )
    select_max = SelectInput(display_text='Select a maximum value',
                             name='select-max',
                             multiple=False,
                             options=[('Unlimited', '1'), ('<5', '2'), ('<2', '3'), ('<1', '4')],
                             initial=['Unlimited']
                             )
    get_Stations = getStations('utah')
    context = {}
    context['all_coords_stations'] = get_Stations['all_coords_stations']
    context['all_stations'] = get_Stations['all_stations']
    context['lake_map'] = get_Stations['lake_map']
    context['select_lake'] = select_lake
    context['select_data'] = select_data
    context['select_parameter'] = select_parameter
    context['select_bdl'] = select_bdl
    context['select_max'] = select_max
    # print(context)
    return render(request, 'lake/home.html', context)


@login_required()
def instructions(request):
    context = {
    }
    return render(request, 'lake/instructions.html', context)


@login_required()
def get_lake(request):
    get_data = request.GET
    lake_name = get_data.get('lake_name')
    # print (lake_name)
    context = lake_name
    stations = getStations(lake_name)
    return JsonResponse(stations)


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
    dataLake = pd.concat(dataLake_all)
    context = {
        'dataLake': dataLake,
        'values_awqms': values_awqms,
        'values_byu': values_byu,
    }

    return context


def getStations(lake_name):

    # Obtner estaciones segun lago para el mapa de estaciones

    dataLake = getFiles(lake_name).get('dataLake')
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
            station = df['Monitoring Location Name'].tolist()[0]
            dataname = str(location)
            context['all_stations'][dataname] = {'coords': [lat, lon], 'org': organization, 'station': station}
    lats = dataLake['Monitoring Location Latitude'].unique()
    lons = dataLake['Monitoring Location Longitude'].unique()
    lats_mean = np.mean(lats)
    lons_mean = np.mean(lons)
    context['all_coords_stations'] = [lats_mean, lons_mean]
    return context


def completeSeries(df):

    # Completar el time series para los graficos

    df['Date'] = pd.to_datetime(df['Activity Start Date'])
    df = df.sort_values(by=['Date'])
    dateslist = df['Date'].tolist()
    inidate = dateslist[0]
    findate = dateslist[-1]
    alldates = []
    curdate = inidate
    while curdate <= findate:
        alldates.append(curdate)
        curdate = curdate + timedelta(days=1)
    df2 = pd.DataFrame(alldates, columns=['Date'])
    dfjoin = df2.merge(df, on='Date', how='left')
    value = dfjoin['Result Value']
    dates = dfjoin['Date']
    datesString = []
    valuesNumpy = value.to_numpy(value)
    valuesNoNan = np.nan_to_num(valuesNumpy, nan=-999)
    valuesFin = valuesNoNan.tolist()
    for datesX in dates:
        datesString.append(str(datesX).split()[0])
    alldates = datesString
    return valuesFin, alldates


def getData(characteristic, fraction):

    # Obtener datos segun el parametro y su fraccion, mandar datos con el timeseries completo

    dataLake = getFiles()
    param = dataLake['Characteristic Name'] == characteristic
    row_param = dataLake[param]
    # check Total-Dissolved
    fract = row_param[row_param['Sample Fraction'] == fraction]
    if len(fract) > 0:
        fract = row_param['Sample Fraction'] == fraction
        row = row_param[fract]
        # print(row)
    else:
        row = row_param

    locations = row['Monitoring Location ID'].unique()
    unit = row['Result Unit'].unique()
    context = {}
    context['characteristic'] = characteristic
    context['fraction'] = fraction
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
            # print(responseObject)
            context['all_data'][dataname] = {'coords': [lat, lon], 'org': organization, 'data': responseObject}
    lats = dataLake['Monitoring Location Latitude'].unique()
    lons = dataLake['Monitoring Location Longitude'].unique()
    lats_mean = np.mean(lats)
    lons_mean = np.mean(lons)
    context['all_coords'] = [lats_mean, lons_mean]
    return context


# def charts(request):
#     timeseries_plot = TimeSeries(
#         height='500px',
#         width='500px',
#         engine='highcharts',
#         title='Irregular Timeseries Plot',
#         y_axis_title='Snow depth',
#         y_axis_units='m',
#         series=[{
#             'name': 'Winter 2007-2008',
#             'data': [
#                 [datetime(2008, 12, 2), 0.8],
#                 [datetime(2008, 12, 9), 0.6],
#                 [datetime(2008, 12, 16), 0.6]
#             ]
#         }]
#     )
#
#     context = {
#                 'timeseries_plot': timeseries_plot,
#               }

def chl_a(request):
    context = getData('Chlorophyll a, uncorrected for pheophytin', ' ')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def do(request):
    context = getData('Dissolved oxygen (DO)', ' ')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def magn_total(request):
    context = getData('Magnesium', 'Total')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def magn_dis(request):
    context = getData('Magnesium', 'Dissolved')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def nit_total(request):
    context = getData('Nitrogen', 'Total')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def nit_dis(request):
    context = getData('Nitrogen', 'Dissolved')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def ph(request):
    context = getData('pH', ' ')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def phosp_total(request):
    context = getData('Phosphate-phosphorus', 'Total')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def phosp_dis(request):
    context = getData('Phosphate-phosphorus', 'Dissolved')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def water_temp(request):
    context = getData('Temperature, water', ' ')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def tds(request):
    context = getData('Total dissolved solids', 'None')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def turb(request):
    context = getData('Turbidity', ' ')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def secchi(request):
    context = getData('Depth, Secchi disk depth', ' ')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)


def ortho(request):
    context = getData('Ortho Phosphorus', 'None')
    download_button = download()

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)
