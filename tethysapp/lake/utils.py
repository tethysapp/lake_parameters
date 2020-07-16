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
