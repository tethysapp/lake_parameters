from django.shortcuts import render
from django.shortcuts import reverse
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button
from tethys_sdk.gizmos import TimeSeries
from django.http import HttpResponse, JsonResponse

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
    """
    Controller for the app home page.
    """

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    dataJson = dataLake.to_dict()
    print(dataJson)

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )


    add_data_button = Button(
        display_text='Add Data',
        name='add-data-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('lake:add_data')
    )

    context = {
        'lake_map': lake_map,
        'add_data_button': add_data_button,
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


    add_data_button = Button(
        display_text='Add Data',
        name='add-data-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('lake:add_data')
    )

    context = {
        'lake_map': lake_map,
        'add_data_button': add_data_button
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

def chl_a(request):
    """
    Controller for the Chlorophyll a  page.
    """
    responseObject310 = {}
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Chlorophyll a, uncorrected for pheophytin'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    print(chl_a_id310)
    chl_a310 = chl_a_row[chl_a_id310]
    print(chl_a310)
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    print(responseObject310['values310'])
    responseObject310['date310']=date310.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310
    }

    return render(request, 'lake/chl_a.html', context)

def do(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/do.html', context)

def nit(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/nit.html', context)

def ph(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/ph.html', context)

def phosp(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/phosp.html', context)

def water_temp(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/water_temp.html', context)

def tds(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/tds.html', context)

def turb(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/turb.html', context)

def secchi(request):
    """
    Controller for the Instructions page.
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

    return render(request, 'lake/secchi.html', context)
