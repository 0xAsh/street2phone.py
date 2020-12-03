import sys, getopt, requests, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--APIKEY", help="Google API key. For information on how acquire one refer to: https://developers.google.com/maps/documentation/javascript/get-api-key", type=str)
parser.add_argument("-i", "--inputfile", help="Standardized Excel worksheet used to track location phone numbers. Refer to documentation for formatting guidance.")
parser.add_argument("-o", "--outputfile", help="Output excel file with appended phone numbers. Specify full path for custom location, otherwise the output file will be written to the current working directory.")
parser.add_argument("-a", "--address", help="Address to convert to local phone numbers", type=str)
args = parser.parse_args()

x = (len(sys.argv))
if x == 1:
   print('Usage: address2phone.py [-h/--help] --inputfile <file.xls> --outputfile <out.xls> --APIKEY <GOOGLE API KEY>')

args.address
print(args.address)

payload = {'key': args.APIKEY, 'query': args.address}
longlat = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?", params=payload)

lat = longlat.json()['results'][0]['geometry']['location']['lat']
lng = longlat.json()['results'][0]['geometry']['location']['lng']
