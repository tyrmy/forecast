import requests
from xml.etree import ElementTree

url = 'http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::timevaluepair&place=turku&parameters=temperature&'

r = requests.get(url)
print(r.status_code)
print("----------")

tree = ElementTree.fromstring(r.content)
#print(tree)
#print(tree.tag)

for child in tree[0][0][-1][0]:
    #print(child.tag)
    print('{}:\t{}'.format(child[0][0].text, child[0][1].text))
