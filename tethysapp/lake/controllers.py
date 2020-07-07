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

# from .utils import selectLake
#
# @login_required()
# def base(request):
#
#     context = selectLake()
#     return render(request, 'lake/base.html', context)

@login_required()
def home(request):
    context = getStations()
    return render(request, 'lake/home.html', context)

@login_required()
def search_data(request):
    context = getStations()
    return render(request, 'lake/search_data.html', context)

@login_required()
def instructions(request):
    context = {
    }

    return render(request, 'lake/instructions.html', context)



def getFiles():
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_utahlake.csv")
    file_path_miller = os.path.join(app_workspace.path, "Miller_data.csv")
    dataLake_awqms = pd.read_csv(file_path)
    dataLake_miller = pd.read_csv(file_path_miller)
    dataLake_miller['Organization ID'] = 'BYU, Dr Miller'
    values_awqms = dataLake_awqms[['Activity Start Date', 'Organization ID', 'Monitoring Location ID', 'Monitoring Location Name', 'Monitoring Location Latitude', 'Monitoring Location Longitude', 'Monitoring Location Type', 'Characteristic Name', 'Sample Fraction', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']]
    values_miller = dataLake_miller[['Activity Start Date', 'Organization ID', 'Monitoring Location ID', 'Monitoring Location Name', 'Monitoring Location Latitude', 'Monitoring Location Longitude', 'Monitoring Location Type', 'Characteristic Name', 'Sample Fraction', 'Result Value', 'Result Unit', 'Detection Condition', 'Detection Limit Value1', 'Detection Limit Unit1']]
    dataLake_all = [values_awqms, values_miller]
    dataLake = pd.concat(dataLake_all)
    context = dataLake
    return context

def getStations():
    dataLake = getFiles()
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
    return context

def completeSeries(df):
    df['Date'] = pd.to_datetime(df['Activity Start Date'])
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
    datesString=[]
    valuesNumpy = value.to_numpy(value)
    valuesNoNan = np.nan_to_num(valuesNumpy, nan=-999)
    valuesFin = valuesNoNan.tolist()
    for datesX in dates:
        datesString.append(str(datesX).split()[0])
    alldates = datesString
    return valuesFin, alldates

def getData(characteristic, fraction):
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

    print(row['Sample Fraction'])

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
    context = getData('Chlorophyll a, uncorrected for pheophytin',' ')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def do(request):
    context = getData('Dissolved oxygen (DO)',' ')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def magn_total(request):
    context = getData('Magnesium','Total')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def magn_dis(request):
    context = getData('Magnesium','Dissolved')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def nit_total(request):
    context = getData('Nitrogen','Total')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def nit_dis(request):
    context = getData('Nitrogen','Dissolved')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def ph(request):
    context = getData('pH',' ')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def phosp_total(request):
    context = getData('Phosphate-phosphorus','Total')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def phosp_dis(request):
    context = getData('Phosphate-phosphorus','Dissolved')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def water_temp(request):
    context = getData('Temperature, water',' ')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def tds(request):
    context = getData('Total dissolved solids','None')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def turb(request):
    context = getData('Turbidity',' ')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def secchi(request):
    context = getData('Depth, Secchi disk depth',' ')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)

def ortho(request):
    context = getData('Ortho Phosphorus','None')
    download_button = Button(
        display_text='Download all data',
        icon='glyphicon glyphicon-download-alt',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'dataplacement':'top',
            'title':'Download'
        }
    )

    context['download_button'] = download_button

    return render(request, 'lake/show_data.html', context)
