import requests

from xml.etree import ElementTree

from datetime import datetime
import dateutil.parser as parser

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

mins = mdates.MinuteLocator(interval=30)
hours = mdates.HourLocator(2)
fmt = mdates.DateFormatter('%m-%d %H:%M')

def plot_forecast(city):
    url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place={}&parameters=temperature&'.format(city)

    r = requests.get(url)
    print(r.status_code)
    print("----------")

    tree = ElementTree.fromstring(r.content)

    dates = []
    values = []

    for child in tree[0][0][-1][0]:
        iso = child[0][0].text
        value = float(child[0][1].text)
        datetime = parser.parse(iso)

        values.append(value)
        dates.append(datetime)

    fig, ax = plt.subplots()

    ax.set_title('{}, Ilmatieteen laitos'.format(city))
    ax.set_ylabel('Temperature')
    ax.set_xlabel('Time')

    #ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_locator(mins)
    plt.plot(dates, values)
    fig.autofmt_xdate()
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    plot_forecast('turku')
