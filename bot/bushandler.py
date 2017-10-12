import json
import urllib
import httplib2 as http
import pandas as pd


# If user choose to know all Bus Service arriving @ her chosen Bus Stop
# return array
# If user choose to know a particular service number @ her chosen Bus Stop
# Return lists of service numbers for inline markup/button PURPOSE (Make inline markup/button with label from service numbers)
# Then user choose the desired Service No using inline markup/button.
# Then, the inline markup/button callback_query send input to getOneArrival INDICATING SERVICE NO. Why separate? because user also inputs are in seperate process

    # A function that takes in bus stop code as an input argument
    # Returns a list of bus services that is currently on operation at that bus stop
def getServiceNums(busstopcode):
        # Run a query to the LTA data mall
    jsonObj = getArrivalAPIData(busstopcode)
        #Initialize an empty list
    serviceNums = []

        # Loop through json dictionary for the bus services
    for i in range(len(jsonObj['Services'])):
        serviceNo = jsonObj['Services'][i]['ServiceNo']
        serviceNums.append(serviceNo)
            # Appending it to the empty list

    return serviceNums

    # A function that takes in a bus stop code and a service number
    # Returns two separate lists:
    # 1. InfoList : Ready to-be displayed arrival information(s)
    # 2. completeTime :  A list of arrival times, complete with the date ...
    #     ... to be operated upon to on the getTime.py module to display a time difference
def getOneArrival(busstopcode, serviceNo):
    jsonObj = getArrivalAPIData(str(busstopcode))
    serviceNo = str(serviceNo)

        # Casting our jsonObj as a DataFrame to ease value-based indexing (refer to the next line)
    df = pd.DataFrame(jsonObj['Services'])
        # Set the service numbers as the index of our dataset so we can call based on it
    df.set_index('ServiceNo', inplace=True)

        # Set all info
    operator = df.loc[serviceNo]['Operator']
    arrival1 = df.loc[serviceNo]['NextBus']['EstimatedArrival'][11:16]
    arrival2 = df.loc[serviceNo]['NextBus2']['EstimatedArrival'][11:16]
    arrival3 = df.loc[serviceNo]['NextBus3']['EstimatedArrival'][11:16]

    withdate1 = df.loc[serviceNo]['NextBus']['EstimatedArrival'][0:-6]
    withdate2 = df.loc[serviceNo]['NextBus2']['EstimatedArrival'][0:-6]
    withdate3 = df.loc[serviceNo]['NextBus3']['EstimatedArrival'][0:-6]

        # Put all info into two separate list
    infoList = [operator, arrival1, arrival2, arrival3]
    completeTime = [withdate1,withdate2,withdate3]

    return infoList, completeTime


# Our getAPIData method for Arrival Information.
def getArrivalAPIData(busstopcode):

    headers = {'AccountKey': 'eLrFcQbtSCOg+3r1yhE4jg==',
               'accept': 'application/json'
               }

    uri = 'http://datamall2.mytransport.sg'
    arrvpath = '/ltaodataservice/BusArrivalv2?BusStopCode='
    busstopcode=str(busstopcode)

    target = urllib.parse.urlparse(uri + arrvpath + busstopcode)
    print(target.geturl())
    method = 'GET'
    body = ''

    h = http.Http()

    response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)

    jsonObj = json.loads(content.decode('utf-8'))
    return jsonObj

