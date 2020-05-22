"""
Created on 18th May 2020
@author Lassi Lehtinen

Fetch data from ilmatieteen laitos and analyze the data
"""
from owslib.wfs import WebFeatureService

if __name__ == "__main__":
    wfs = WebFeatureService(url='https://opendata.fmi.fi/wfs?request=GetCapabilities', version='2.0.0')
    print(wfs.identification.title)
    #wfs.get_schema('BsWfs:BsWfsElement')
    #for idx, storedquery in enumerate(wfs.storedqueries):
    #    print(idx, ': ', storedquery.id, ' -- ', storedquery.title)
    #print(list(wfs.contents))

    storedquery = wfs.storedqueries[26]
    print('\nStoredQuery parameters for %s' % storedquery.id)
    for parameter in storedquery.parameters:
        print(parameter.name, parameter.type)

    #exit()
    print('\nDownload data from %s' % wfs.identification.title)
    response = wfs.getfeature(
            storedQueryID='fmi::forecast::hirlam::surface::cities::timevaluepair',
            #storedQueryID='fmi::forecast::hirlam::surface::cities::multipointcoverage',
            #storedQueryID='fmi::forecast::hirlam::surface::cities::simple',
            storedQueryParams={'timestep':'60', 
                                'parameters':'temperature', 
                                'maxlocations':'1', 
                                'starttime':'2020-05-21T00:00:00Z',
                                'endtime':'2020-05-22T00:00:00Z',
                                'geoid':'633679'
                                })
    s = response.read().decode()
    print(s)
    print('... done')
