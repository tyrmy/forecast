import requests
from xml.etree import ElementTree

url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place=turku&parameters=temperature&'

r = requests.get(url)
print(r.status_code)

tree = ElementTree.fromstring(r.content)
#print(tree)
