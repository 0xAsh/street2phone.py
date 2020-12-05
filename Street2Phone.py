import argparse
import sys
from collections import Counter
from collections import deque
import requests
import xlrd
from xlutils.copy import copy

## Parser Documentation
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--APIKEY", help="Google API key. For information on how acquire one refer to: https://developers.google.com/maps/documentation/javascript/get-api-key", type=str)
parser.add_argument("-i", "--inputfile", help="Standardized Excel worksheet used to track location phone numbers. Refer to documentation for formatting guidance.")
parser.add_argument("-o", "--outputfile", help="Output excel file with appended phone numbers. Specify full path for custom location, otherwise the output file will be written to the current working directory.")
parser.add_argument("-a", "--address", help="Address to convert to local phone numbers", type=str)
args = parser.parse_args()

## Friendly Error Checking
if len(sys.argv) == 1:
    print('Usage: address2phone.py [-h/--help] --inputfile <file.xls> --outputfile <out.xls> --APIKEY <GOOGLE API KEY>')
elif len(sys.argv) != 1:
    if args.APIKEY is None:
        print('Please provide APIKEY via the --APIKEY/-k argument\n')
    if args.inputfile is None:
        print('Please provide name of input Excel file via the --inputfile/-i argument')
        print('If the Excel file is located within a different directory, please specify the full file path\n')
    if args.outputfile is None:
        print('Please provide output Excel file name via the --outputfile/-o argument\n')

## Lat/Long Gathering
def getLatLng(addr):
   latlongPayload = {'key': args.APIKEY, 'query': addr, 'fields': "lat,lng"}
   longlat = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?", params=latlongPayload)
   try:
      lat = longlat.json()['results'][0]['geometry']['location']['lat']
      lng = longlat.json()['results'][0]['geometry']['location']['lng']
      return str(lat) + "," + str(lng)
   except (IndexError, UnboundLocalError):
         print("No lat long found")
         pass

## PlaceID Gathering
def getPlaceIDs():
   nearbyPayload = {'key': args.APIKEY, 'location': getLatLng(address), 'radius': 150}
   nearbyReq = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params=nearbyPayload)
   nearbysearches = nearbyReq.json()['results']
   placeIDList = []
   
   ## Iterate through JSON and add place_ids to list is not empty
   for i in nearbysearches:
      if i['place_id'] is not None:
         placeIDList.append(i['place_id'])

   return placeIDList

## Generate a list of nearby phone numbers using the list of place IDs from getPlaceIDs()
def makePhoneNumberList():
   phoneNumsList = []
   for i in getPlaceIDs():
      placeIDpayload = {'key': args.APIKEY, 'place_id': i, 'fields': "formatted_phone_number"}
      phoneQuery = requests.get('https://maps.googleapis.com/maps/api/place/details/json?', params=placeIDpayload)
      phoneNumbs = phoneQuery.json()['result']
      phoneNumsList.append(phoneNumbs.get("formatted_phone_number"))
      
   return phoneNumsList

## Finds the most common first six digits of a phone number from a list of numbers (phoneList)
## Returns a phone number within that list that possesses the same first six most common digits

def mostCommon(phoneList):
   tempList = []
   for i in filter(None, phoneList):
      tempList.append(i[0:9])
   d = Counter(tempList).most_common()
   try:
      commonSix = d[0][0]
      for x in filter(None, phoneList):
         if x[0:9] == commonSix:
            return(x)
   except IndexError:
      pass


## Main Function
excelFile = xlrd.open_workbook(args.inputfile)
excelSheet = excelFile.sheet_by_index(0)
excelCopy = copy(excelFile)
copySheet = excelCopy.get_sheet(0)

i = 1 

while i < excelSheet.nrows:
    address = (str(excelSheet.cell(i, 4).value) + ", " + str(excelSheet.cell(i, 6).value) + ", " + str(excelSheet.cell(i, 7).value) + " " + str(excelSheet.cell(i, 8).value))
    
    print(address)
    print(getPlaceIDs())
    print(makePhoneNumberList())
    print(mostCommon(makePhoneNumberList()))

    copySheet.write(i, 9, mostCommon(makePhoneNumberList()))
    print(i)
    print(excelSheet.nrows)
    i += 1

excelCopy.save(args.outputfile)
