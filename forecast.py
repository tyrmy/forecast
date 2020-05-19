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

def plot_forecast(city):
    """ Fetch data from ilmatieteen laitos and plot results for a city specified """
    url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place={}&parameters=temperature&endtime=2020-05-21T00:00Z'.format(city)
    #url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place={}&parameters=temperature&'.format(city)

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

    # Create dataframe
    df = pd.DataFrame()
    df['temperature'] = smoothen
    df['datetime'] = dates
    df = df.set_index('datetime')

    # Group by dates and find local maximum
    tmax = df.loc[df.groupby(pd.Grouper(freq='D')).idxmax().iloc[:,0]]
    tmax = tmax.reset_index()

    # Group by dates and find local minimum
    tmin = df.loc[df.groupby(pd.Grouper(freq='D')).idxmin().iloc[:,0]]
    tmin = tmin.reset_index()

    # Create figure
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_ylim(bottom=-5, top=20)

    # Plot line, max and min scatter
    df.plot(y='temperature',
            title="Ennuste {}".format(city),
            ax=ax)
    tmax.plot.scatter(y='temperature',
            x='datetime',
            c='red',
            s=50,
            ax=ax)
    tmin.plot.scatter(y='temperature',
            x='datetime',
            c='blue',
            s=50,
            ax=ax)

    plt.grid(True)
    plt.show()

def plot_forecasts(citys):
    """ Fetch data from ilmatieteen laitos and plot results for a city specified """
    # Create figure
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_ylim(bottom=-5, top=20)

    for city in citys:
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

        # Create dataframe
        df = pd.DataFrame()
        df['temperature'] = values
        df['datetime'] = dates
        df = df.set_index('datetime')

        # Group by dates and find local maximum
        tmax = df.loc[df.groupby(pd.Grouper(freq='D')).idxmax().iloc[:,0]]
        tmax = tmax.reset_index()

        # Group by dates and find local minimum
        tmin = df.loc[df.groupby(pd.Grouper(freq='D')).idxmin().iloc[:,0]]
        tmin = tmin.reset_index()

        # Plot line, max and min scatter
        df.plot(y='temperature',
                ax=ax)
        tmax.plot.scatter(y='temperature',
                x='datetime',
                c='red',
                s=50,
                ax=ax)
        tmin.plot.scatter(y='temperature',
                x='datetime',
                c='blue',
                s=50,
                ax=ax)

    ax.legend(citys)
    plt.grid(True)
    plt.title("Ilmatieteenlaitos, ennusteet")
    plt.show()

if __name__ == "__main__":
    citys = ['kuopio', 'rauma', 'turku', 'helsinki', 'tampere', 'vantaa']
    plot_forecasts(citys)
