"""
Created on 18th May 2020
@author Lassi Lehtinen

Fetch data from ilmatieteen laitos and analyze the data
"""
import requests

from xml.etree import ElementTree

from datetime import datetime, timedelta
import dateutil.parser as parser

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scipy.signal import savgol_filter
import pandas as pd

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))

def grid_forecasts(citys):
    """ Fetch data from ilmatieteen laitos and plot results for a city specified """
    # Create figure
    fig, ax = plt.subplots(2,2, figsize=(7,7))
    axes = ax.flatten()
    param = 'temperature'

    for idx, city in enumerate(citys):
        url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::harmonie::hybrid::point::simple&place={city}&parameters={param}&timestep=30'.format(city=city, param=param)
        r = requests.get(url)
        print(city)
        print('Success %r' % r)
        print('Elapsed time: ', r.elapsed)
        print('Status code:, ', r.status_code)
        print('Code status: ', r.reason)
        print("----------")

        dates = []
        values = []

        tree = ElementTree.fromstring(r.content)
        # Parse dates and values form xml
        for child in tree:
            iso = child[0][1].text
            temp = float(child[0][3].text)
            datetime = parser.parse(iso) + timedelta(hours=3)
            #print(datetime.strftime("%m/%d/%Y, %H:%M:%S"), ': ', temp)
            values.append(temp)
            dates.append(datetime)

        # Create dataframe
        df = pd.DataFrame()
        df['temperature'] = values
        df['datetime'] = dates
        df = df.set_index('datetime')
        axes[idx].set_ylim(bottom=5, top=20)
        axes[idx].grid(True, color='r')
        axes[idx].set_title(city)

        # Group by dates and find local maximum
        tmax = df.loc[df.groupby(pd.Grouper(freq='D')).idxmax().iloc[:,0]]
        tmax = tmax.reset_index()

        # Group by dates and find local minimum
        tmin = df.loc[df.groupby(pd.Grouper(freq='D')).idxmin().iloc[:,0]]
        tmin = tmin.reset_index()

        # Plot line, max and min scatter
        df.plot(y='temperature',
                grid=True,
                ax=axes[idx])
        tmax.plot.scatter(y='temperature',
                x='datetime',
                c='red',
                s=50,
                ax=axes[idx])
        tmin.plot.scatter(y='temperature',
                x='datetime',
                c='blue',
                s=50,
                ax=axes[idx])

    fig.suptitle("Ilmatieteenlaitos, ennusteet")
    plt.show()


def plot_forecasts(citys):
    """ Fetch data from ilmatieteen laitos and plot results for a city specified """
    # Create figure
    fig, ax = plt.subplots(figsize=(7,7))
    param = 'temperature'

    for idx, city in enumerate(citys):
        url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::harmonie::hybrid::point::simple&place={city}&parameters={param}&timestep=30'.format(city=city, param=param)
        r = requests.get(url)
        print(city)
        print('Success %r' % r)
        print('Elapsed time: ', r.elapsed)
        print('Status code:, ', r.status_code)
        print('Code status: ', r.reason)
        print("----------")

        dates = []
        values = []

        tree = ElementTree.fromstring(r.content)
        # Parse dates and values form xml
        for child in tree:
            iso = child[0][1].text
            temp = float(child[0][3].text)
            datetime = parser.parse(iso) + timedelta(hours=3)
            values.append(temp)
            dates.append(datetime)

        # Create dataframe
        df = pd.DataFrame()
        df['temperature'] = values
        df['datetime'] = dates
        df = df.set_index('datetime')
        ax.set_ylim(bottom=5, top=25)

        # Group by dates and find local maximums
        tmax = df.loc[df.groupby(pd.Grouper(freq='D')).idxmax().iloc[:,0]]
        tmax = tmax.reset_index()

        # Group by dates and find local minimums
        tmin = df.loc[df.groupby(pd.Grouper(freq='D')).idxmin().iloc[:,0]]
        tmin = tmin.reset_index()

        # Plot line, max and min scatter
        df.plot(y='temperature',
                grid=True,
                ax=ax)
        tmax.plot.scatter(y='temperature',
                x='datetime',
                c='red',
                s=40,
                ax=ax)
        tmin.plot.scatter(y='temperature',
                x='datetime',
                c='blue',
                s=30,
                ax=ax)

        # Draw min and max values to plot
        label_point(tmin.datetime, tmin.temperature, tmin.temperature, ax)
        label_point(tmax.datetime, tmax.temperature, tmax.temperature, ax)

    ax.grid(True)
    plt.legend(citys)
    fig.suptitle("Ilmatieteenlaitos, ennusteet")
    plt.show()

if __name__ == "__main__":
    citys = ['Kuopio', 'Rauma', 'Turku']
    plot_forecasts(citys)
