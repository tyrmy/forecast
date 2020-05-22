"""
Created on 18th May 2020
@author Lassi Lehtinen

Fetch data from ilmatieteen laitos and analyze the data
"""
from owslib.wfs import WebFeatureService

if __name__ == "__main__":
    wfs = WebFeatureService(url='https://opendata.fmi.fi/wfs?request=GetCapabilities', version='2.0.0')
    print(wfs.identification.title)
    for idx, storedquery in enumerate(wfs.storedqueries):
        print(idx, ': ', storedquery.id, ' -- ', storedquery.title)

    storedquery = wfs.storedqueries[104]
    print('\nStoredQuery parameters for %s' % storedquery.id)
    for parameter in storedquery.parameters:
        print(parameter.name, parameter.type)

    #exit()
    print('\nDownload data from %s' % wfs.identification.title)
    response = wfs.getfeature(
            storedQueryID='fmi::observations::weather::multipointcoverage',
            #storedQueryID='fmi::forecast::hirlam::surface::cities::multipointcoverage',
            #storedQueryID='fmi::forecast::hirlam::surface::cities::simple',
            storedQueryParams={'place':'Turku', 
                                'parameters':'temperature,humidity,pressure,totalcloudcover', 
                                })
    s = response.read().decode()
    print(s)
    print('... done')
