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
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Chlorophyll a, uncorrected for pheophytin'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/chl_a.html', context)

def do(request):
    """
    Controller for the do page.
    """
    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Dissolved oxygen (DO)'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/do.html', context)

def nit(request):
    """
    Controller for the Nitrogen page.
    """

    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Nitrogen'
    chl_a_both = dataLake[chl_a_param]
    chl_a_total = chl_a_both['Sample Fraction']=='Total'
    chl_a_row = chl_a_both[chl_a_total]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/nit.html', context)

def ph(request):
    """
    Controller for the ph page.
    """

    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='pH'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/ph.html', context)

def phosp(request):
    """
    Controller for the Phosphorus page.
    """
    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Phosphate-phosphorus'
    chl_a_both = dataLake[chl_a_param]
    chl_a_total = chl_a_both['Sample Fraction']=='Total'
    chl_a_row = chl_a_both[chl_a_total]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/phosp.html', context)

def water_temp(request):
    """
    Controller for the Water Temp page.
    """
    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Temperature, water'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/water_temp.html', context)

def tds(request):
    """
    Controller for the TDS page.
    """
    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Total dissolved solids'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/tds.html', context)

def turb(request):
    """
    Controller for the Turbidity page.
    """
    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Turbidity'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/turb.html', context)

def secchi(request):
    """
    Controller for the Secchi Disk page.
    """
    responseObject310 = {}
    responseObject365 = {}
    responseObject370 = {}
    responseObject390 = {}
    responseObject450 = {}
    responseObject500 = {}
    responseObject520 = {}
    responseObject600 = {}
    responseObject700 = {}
    responseObject710 = {}
    responseObject715 = {}
    responseObject770 = {}

    app_workspace = app.get_app_workspace()
    file_path = os.path.join(app_workspace.path,"awqms_lake.csv")
    dataLake = pd.read_csv(file_path)
    chl_a_param = dataLake['Characteristic Name']=='Depth, Secchi disk depth'
    chl_a_row = dataLake[chl_a_param]

    chl_a_id310 = chl_a_row['Monitoring Location ID']==4917310
    chl_a310 = chl_a_row[chl_a_id310]
    value310 = chl_a310['Result Value']
    date310 = chl_a310['Activity Start Date']
    valuesNumpy310 = value310.to_numpy()
    valuesNoNan310 = np.nan_to_num(valuesNumpy310)
    valuesFin310 = valuesNoNan310.tolist()
    responseObject310['values310']=valuesFin310
    responseObject310['date310']=date310.to_numpy().tolist()

    chl_a_id365 = chl_a_row['Monitoring Location ID']==4917365
    chl_a365 = chl_a_row[chl_a_id365]
    value365 = chl_a365['Result Value']
    date365 = chl_a365['Activity Start Date']
    valuesNumpy365 = value365.to_numpy()
    valuesNoNan365 = np.nan_to_num(valuesNumpy365)
    valuesFin365 = valuesNoNan365.tolist()
    responseObject365['values365']=valuesFin365
    responseObject365['date365']=date365.to_numpy().tolist()

    chl_a_id370 = chl_a_row['Monitoring Location ID']==4917370
    chl_a370 = chl_a_row[chl_a_id370]
    value370 = chl_a370['Result Value']
    date370 = chl_a370['Activity Start Date']
    valuesNumpy370 = value370.to_numpy()
    valuesNoNan370 = np.nan_to_num(valuesNumpy370)
    valuesFin370 = valuesNoNan370.tolist()
    responseObject370['values370']=valuesFin370
    responseObject370['date370']=date370.to_numpy().tolist()

    chl_a_id390 = chl_a_row['Monitoring Location ID']==4917390
    chl_a390 = chl_a_row[chl_a_id390]
    value390 = chl_a390['Result Value']
    date390 = chl_a390['Activity Start Date']
    valuesNumpy390 = value390.to_numpy()
    valuesNoNan390 = np.nan_to_num(valuesNumpy390)
    valuesFin390 = valuesNoNan390.tolist()
    responseObject390['values390']=valuesFin390
    responseObject390['date390']=date390.to_numpy().tolist()

    chl_a_id450 = chl_a_row['Monitoring Location ID']==4917450
    chl_a450 = chl_a_row[chl_a_id450]
    value450 = chl_a450['Result Value']
    date450 = chl_a450['Activity Start Date']
    valuesNumpy450 = value450.to_numpy()
    valuesNoNan450 = np.nan_to_num(valuesNumpy450)
    valuesFin450 = valuesNoNan450.tolist()
    responseObject450['values450']=valuesFin450
    responseObject450['date390']=date450.to_numpy().tolist()

    chl_a_id500 = chl_a_row['Monitoring Location ID']==4917500
    chl_a500 = chl_a_row[chl_a_id500]
    value500 = chl_a500['Result Value']
    date500 = chl_a500['Activity Start Date']
    valuesNumpy500 = value500.to_numpy()
    valuesNoNan500 = np.nan_to_num(valuesNumpy500)
    valuesFin500 = valuesNoNan500.tolist()
    responseObject500['values500']=valuesFin390
    responseObject500['date500']=date390.to_numpy().tolist()

    chl_a_id520 = chl_a_row['Monitoring Location ID']==4917520
    chl_a520 = chl_a_row[chl_a_id520]
    value520 = chl_a520['Result Value']
    date520 = chl_a520['Activity Start Date']
    valuesNumpy520 = value520.to_numpy()
    valuesNoNan520 = np.nan_to_num(valuesNumpy520)
    valuesFin520 = valuesNoNan520.tolist()
    responseObject520['values520']=valuesFin520
    responseObject520['date520']=date520.to_numpy().tolist()

    chl_a_id600 = chl_a_row['Monitoring Location ID']==4917600
    chl_a600 = chl_a_row[chl_a_id600]
    value600 = chl_a600['Result Value']
    date600 = chl_a600['Activity Start Date']
    valuesNumpy600 = value600.to_numpy()
    valuesNoNan600 = np.nan_to_num(valuesNumpy600)
    valuesFin600 = valuesNoNan600.tolist()
    responseObject600['values600']=valuesFin600
    responseObject600['date600']=date600.to_numpy().tolist()

    chl_a_id700 = chl_a_row['Monitoring Location ID']==4917700
    chl_a700 = chl_a_row[chl_a_id700]
    value700 = chl_a700['Result Value']
    date700 = chl_a700['Activity Start Date']
    valuesNumpy700 = value700.to_numpy()
    valuesNoNan700 = np.nan_to_num(valuesNumpy700)
    valuesFin700 = valuesNoNan700.tolist()
    responseObject700['values700']=valuesFin700
    responseObject700['date700']=date700.to_numpy().tolist()

    chl_a_id710 = chl_a_row['Monitoring Location ID']==4917710
    chl_a710 = chl_a_row[chl_a_id710]
    value710 = chl_a710['Result Value']
    date710 = chl_a710['Activity Start Date']
    valuesNumpy710 = value710.to_numpy()
    valuesNoNan710 = np.nan_to_num(valuesNumpy710)
    valuesFin710 = valuesNoNan710.tolist()
    responseObject710['values710']=valuesFin710
    responseObject710['date710']=date710.to_numpy().tolist()

    chl_a_id715 = chl_a_row['Monitoring Location ID']==4917715
    chl_a715 = chl_a_row[chl_a_id715]
    value715 = chl_a715['Result Value']
    date715 = chl_a715['Activity Start Date']
    valuesNumpy715 = value715.to_numpy()
    valuesNoNan715 = np.nan_to_num(valuesNumpy715)
    valuesFin715 = valuesNoNan715.tolist()
    responseObject715['values715']=valuesFin715
    responseObject715['date715']=date715.to_numpy().tolist()

    chl_a_id770 = chl_a_row['Monitoring Location ID']==4917770
    chl_a770 = chl_a_row[chl_a_id770]
    value770 = chl_a770['Result Value']
    date770 = chl_a770['Activity Start Date']
    valuesNumpy770 = value770.to_numpy()
    valuesNoNan770 = np.nan_to_num(valuesNumpy770)
    valuesFin770 = valuesNoNan770.tolist()
    responseObject770['values770']=valuesFin770
    responseObject770['date770']=date770.to_numpy().tolist()

    lake_map = MapView(
        height='100%',
        width='100%',
        layers=[],
        basemap='OpenStreetMap',
    )

    context = {
        'lake_map': lake_map,
        'csvLake':dataLake,
        'data310':responseObject310,
        'data365':responseObject365,
        'data370':responseObject370,
        'data390':responseObject390,
        'data450':responseObject450,
        'data500':responseObject500,
        'data520':responseObject520,
        'data600':responseObject600,
        'data700':responseObject700,
        'data710':responseObject710,
        'data715':responseObject715,
        'data770':responseObject770,
    }

    return render(request, 'lake/secchi.html', context)
