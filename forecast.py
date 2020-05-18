"""
Created on 18th May 2020
@author Lassi Lehtinen

Fetch data from ilmatieteen laitos and analyze the data
"""
import requests

from xml.etree import ElementTree

from datetime import datetime
import dateutil.parser as parser

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scipy.signal import savgol_filter
import pandas as pd

mins = mdates.MinuteLocator(interval=30)
hours = mdates.HourLocator(2)
fmt = mdates.DateFormatter('%m-%d %H:%M')

def plot_forecast(city):
    """ Fetch data from ilmatieteen laitos and plot results for a city specified """
    url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place={}&parameters=temperature&endtime=2020-05-21T00:00Z'.format(city)

    r = requests.get(url)
    print(r.status_code)
    print("----------")

    tree = ElementTree.fromstring(r.content)

    dates = []
    values = []

    # Parse dates and values form xml
    for child in tree[0][0][-1][0]:
        iso = child[0][0].text
        value = float(child[0][1].text)
        datetime = parser.parse(iso)

        values.append(value)
        dates.append(datetime)

    # Apply savgol filter
    smoothen = savgol_filter(values, 7, 3)


    df = pd.DataFrame()
    df['temperature'] = smoothen
    df['datetime'] = dates

    df.plot(y='temperature', x='datetime')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_forecast('turku')
