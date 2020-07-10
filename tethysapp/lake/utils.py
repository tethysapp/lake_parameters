from tethys_sdk.gizmos import SelectInput, Button
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

def get_select_lake():
    select_lake = SelectInput(display_text='Select a Lake',
                            name='select-lake',
                            multiple=False,
                            options=[('Utah Lake','1'), ('Salt Lake','2')],
                            initial=['Utah Lake']
                            )

    return select_lake
