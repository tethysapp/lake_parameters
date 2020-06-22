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


def getData(file_path, characteristic):
    dataLake = pd.read_csv(file_path)
    param = dataLake['Characteristic Name'] == characteristic
    row = dataLake[param]
    locations = dataLake['Monitoring Location ID'].unique()
    locations.sort()
    context = {}
    context['csvLake'] = dataLake
    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )
    context['lake_map'] = lake_map
    for location in locations:
        lastthree = str(location)[-3:]
        # lastthree = str(location)
        valuesname = "values" + lastthree
        datename = "date" + lastthree
        dataname = "data" + lastthree
        charac_id = row['Monitoring Location ID'] == location
        charac = row[charac_id]
        value = charac['Result Value']
        date = charac['Activity Start Date']
        valuesNumpy = value.to_numpy()
        valuesNoNan = np.nan_to_num(valuesNumpy)
        valuesFin = valuesNoNan.tolist()
        responseObject = {}
        responseObject[valuesname] = valuesFin
        responseObject[datename] = date.to_numpy().tolist()
        context[dataname] = responseObject
    return context


def chl_a(request):
    """
    Controller for the Chlorophyll a  page.
    """
    characteristic = "Chlorophyll a, uncorrected for pheophytin"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/chl_a.html', context)

def do(request):
    """
    Controller for the do page.
    """
    characteristic = "Dissolved oxygen (DO)"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/do.html', context)


def nit(request):
    """
    Controller for the Nitrogen page.
    """
    characteristic = "Nitrogen"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/nit.html', context)

    # chl_a_param = dataLake['Characteristic Name']=='Nitrogen'
    # chl_a_both = dataLake[chl_a_param]
    # chl_a_total = chl_a_both['Sample Fraction']=='Total'
    # chl_a_row = chl_a_both[chl_a_total]


def ph(request):
    """
    Controller for the ph page.
    """
    characteristic = "pH"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/ph.html', context)


def phosp(request):
    """
    Controller for the Phosphorus page.
    """
    characteristic = "Phosphate-phosphorus"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/phosp.html', context)

    # chl_a_param = dataLake['Characteristic Name']=='Phosphate-phosphorus'
    # chl_a_both = dataLake[chl_a_param]
    # chl_a_total = chl_a_both['Sample Fraction']=='Total'
    # chl_a_row = chl_a_both[chl_a_total]


def water_temp(request):
    """
    Controller for the Water Temp page.
    """
    characteristic = "Temperature, water"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/water_temp.html', context)


def tds(request):
    """
    Controller for the TDS page.
    """
    characteristic = "Total dissolved solids"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/tds.html', context)


def turb(request):
    """
    Controller for the Turbidity page.
    """
    characteristic = "Turbidity"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/turb.html', context)


def secchi(request):
    """
    Controller for the Secchi Disk page.
    """
    characteristic = "Depth, Secchi disk depth"
    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path, "awqms_lake.csv")
    context = getData(file_path, characteristic)
    return render(request, 'lake/secchi.html', context)
