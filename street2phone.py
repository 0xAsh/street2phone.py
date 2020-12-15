import argparse
import sys
from collections import Counter
from collections import deque
import requests

## Parser Documentation
parser = argparse.ArgumentParser()
parser.add_argument("-k", "--APIKEY", help="Google API key. For information on how acquire one refer to: https://developers.google.com/maps/documentation/javascript/get-api-key", type=str)
parser.add_argument("-i", "--inputfile", help="Input file containing a newline separated list of addresses")
parser.add_argument("-o", "--outputfile", help="Name of output file containing comma-delimmited list addresses and a given phone number")
parser.add_argument("-a", "--address", help="Address to convert to local phone numbers", type=str)
args = parser.parse_args()

## Error Checking
if len(sys.argv) == 1:
    print('Usage: address2phone.py [-h/--help] --APIKEY/-k <GOOGLE API KEY> --inputfile/-i <file> --outputfile/-o <outfile> --address/-a <Address to Lookup>')
elif len(sys.argv) != 1:
    if args.APIKEY is None:
        print('Please provide APIKEY via the --APIKEY/-k argument\n')
        quit()
    if args.inputfile or args.address is not None:
        pass
    else:
        print(type(args.address))
        print(type(args.inputfile))
        print('Please provide an address via or -a or an input file via -i\n')
        quit()
    if args.inputfile is not None and args.outputfile is None:
        print('Please provide output file name via the --outputfile/-o argument\n')
        quit()

## Lat/Long Gathering
def getLatLng(addr):
   latlongPayload = {'key': args.APIKEY, 'query': addr, 'fields': "lat,lng"}
   longlat = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?", params=latlongPayload)
   try:
      lat = longlat.json()['results'][0]['geometry']['location']['lat']
      lng = longlat.json()['results'][0]['geometry']['location']['lng']
      return str(lat) + "," + str(lng)
   ## Catch errors
   except (IndexError, UnboundLocalError):
         print("No lat long found")
         pass

## PlaceID Gathering
def getPlaceIDs(addr):
   nearbyPayload = {'key': args.APIKEY, 'location': getLatLng(addr), 'radius': 150}
   nearbyReq = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?", params=nearbyPayload)
   nearbysearches = nearbyReq.json()['results']
   placeIDList = []
   
   ## Iterate through JSON and add place_ids to list if not empty
   for i in nearbysearches:
      if i['place_id'] is not None:
         placeIDList.append(i['place_id'])

   return placeIDList

## Generate a list of nearby phone numbers using the list of place IDs from getPlaceIDs()
def makePhoneNumberList():
   phoneNumsList = []
   for i in getPlaceIDs(address):
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


## Main Functions

if args.address is not None:
   address = args.address
   print("Lookup Address: " + address + "\n")
   ##print(getPlaceIDs(address))
   print("List of nearby phone numbers: ")
   tempPhoneList = makePhoneNumberList()
   print(tempPhoneList)

   print("\nLocal phone number with the most common first six digits: ")
   print(mostCommon(tempPhoneList))

if args.inputfile is not None:
   file = open(args.inputfile, 'r')
   Lines = file.readlines()
   
   ## Setup outfile and headers
   outFile = open(args.outputfile, "a")

   for line in Lines:
      ## Set address to current line
      ## This is kinda dumb using a hardcoded variable of address in all the functions but w/e
      address = line
      print("Lookup Address: " + address + "\n")

      ## get current list of nearby phone numbs and assign to variable
      print("List of nearby phone numbers: ")
      tempPhoneList = makePhoneNumberList()
      print(tempPhoneList)

      
      ## Run the mostCommon function on the list variable
      print("\nLocal phone number with the most common first six digits: ")
      commonNum = mostCommon(tempPhoneList)
      print(commonNum)

      ## Append current result to outfile
      try:
         outFile.writelines((line + "\t" + commonNum) + "\n")
      except TypeError:
         pass
   outFile.close()
