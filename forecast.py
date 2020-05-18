import requests
from xml.etree import ElementTree
from datetime import datetime
import dateutil.parser as parser
import matplotlib.pyplot as plt

url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place=turku&parameters=temperature&'

r = requests.get(url)
print(r.status_code)
print("----------")

tree = ElementTree.fromstring(r.content)

dates = []
values = []

for child in tree[0][0][-1][0]:
    #print('{}:\t{}'.format(child[0][0].text, child[0][1].text))
    iso = child[0][0].text
    value = float(child[0][1].text)
    datetime = parser.parse(iso)

    values.append(value)
    dates.append(datetime)

#print(values, dates)
fig, ax = plt.subplots()
ax.set_title('Turun ennuste, Ilmatieteen laitos')
plt.plot(dates, values)
fig.autofmt_xdate()
plt.grid(True)
plt.show()
