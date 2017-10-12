import xml.etree.ElementTree as ET
    # We have partitioned bus stops codes into 9 files, according to their first digit
    # This is as to minimize searching time, as there are 4000+ bus stops in Singapore

    # A function that given a 5-digit numeric string
    # Returns a boolean value:
    # True if we found a match within our database -- meaning that is there is a valid bus stop code
    # False if no match found within our database -- meaning that there is no such bus stop code
def checkBusStop(busstopcode):

    startswith = busstopcode[0]

        #Apply selective parsing - we choose a file to parse based on the bus stop code first digit
    e = ET.parse('/app/bot/busstop' + startswith + '.xml').getroot()
    for atype in e.findall('option'):
        if (busstopcode == atype.get('value')):
            return True  # YES THERE IS SUCH BUS STOP
    return False  # NOT A VALID BUS STOP CODE
