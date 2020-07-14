from tethys_sdk.gizmos import Button
from .app import Lake as app
import plotly.graph_objs as go
import requests
import numpy as np
import pandas as pd
import io
import os
import math

def download():
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

    return download_button

# def get_select_lake():
#     select_lake = SelectInput(display_text='Select a Lake',
#                             name='select-lake',
#                             multiple=False,
#                             options=[('Utah Lake','1'), ('Salt Lake','2')],
#                             initial=['Utah Lake']
#                             )
#     return select_lake
#
# def get_select_data():
#     select_data = SelectInput(display_text='Select Data',
#                             name='select-data',
#                             multiple=False,
#                             options=[('All','1'), ('AWQMS','2'),('BYU','3')],
#                             initial=['All']
#                             )
#     return select_data
#
# def get_select_parameter():
#     select_parameter = SelectInput(display_text='Select a Parameter',
#                             name='select-parameter',
#                             multiple=False,
#                             options=[('Chlorophyll-a','1'), ('Dissolved Oxygen','2'),('Phosphate-phosphorus','3'),('Nitrogen','4'),('Magnesium','5'),('Ortho Phosphorus','6'),('pH','7'),('Water Temperature','8'),('Turbidity','9'),('Secchi Disk Depth','10'),('Total Dissolved Solids','11')],
#                             initial=['Chlorophyll-a']
#                             )
#     return select_parameter
#
# def get_select_bdl():
#     select_bdl = SelectInput(display_text='Select a value for Data below Detection Limit',
#                             name='select-bdl',
#                             multiple=False,
#                             options=[('0','1'), ('Detection Limit','2'),('1/2 Detection Limit','3')],
#                             initial=['0']
#                             )
#     return select_bdl
#
# def get_select_max():
#     select_max = SelectInput(display_text='Select a maximum value',
#                             name='select-max',
#                             multiple=False,
#                             options=[('Unlimited','1'), ('<5','2'),('<2','3'),('<1','4')],
#                             initial=['Unlimited']
#                             )
#     return select_max
