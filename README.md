Automates usage of the [Google Places API](https://developers.google.com/places/web-service/overview) to farm local phone numbers given an address.

For more info read the related [blog post](https://0xash.io/2020-12-14-Farming-phone-numbers-with-Python-and-the-Google-Places-API/).

![header](street2phone2.png)

## Installation:
```
git clone https://github.com/0xAsh/street2phone.py
pip install -r requirements.txt
```

## Usage:

```python
usage: street2phone.py [-h] [-k APIKEY] [-i INPUTFILE] [-o OUTPUTFILE] [-a ADDRESS]

arguments:
  -h, --help            show this help message and exit
  -k APIKEY, --APIKEY APIKEY
                        Google API key. For information on how acquire one refer to: https://developers.google.com/maps/documentation/javascript/get-api-key
  -i INPUTFILE, --inputfile INPUTFILE
                        Input file containing a newline separated list of addresses
  -o OUTPUTFILE, --outputfile OUTPUTFILE
                        Name of output file containing comma-delimmited list addresses and a given phone number
  -a ADDRESS, --address ADDRESS
                        Address to convert to local phone numbers
```

### Example output with a single address:
```bash
> python .\Street2Phone.py -k <apikey> -a "1600 Pennsylvania Ave NW, Washington, DC 20500-0003, United States"
Lookup Address: 1600 Pennsylvania Ave NW, Washington, DC 20500-0003, United States

List of nearby phone numbers:
[None, None, '(202) 456-1111', '(202) 456-1414', None, '(202) 456-1414', None, '(800) 488-3111', None, '(987) 654-3210', None, None, None, '(202) 555-0133', '(202) 456-1111', '(202) 456-1111', None, None]

Local phone number with the most common first six digits:
(202) 456-1111
```
### Example output with a list of newline-delimited addresses:
```bash
> python .\street2phone.py -k <apikey> -i .\addresses.txt -o phonenumbers.txt
Lookup Address: 1600 Pennsylvania Ave NW, Washington, DC 20500-0003, United States


List of nearby phone numbers:
[None, None, '(202) 456-1111', '(202) 456-1414', None, '(202) 456-1414', None, '(800) 488-3111', None, '(987) 654-3210', None, None, None, '(202) 555-0133', '(202) 456-1111', '(202) 456-1111', None, None]

Local phone number with the most common first six digits:
(202) 456-1111
Lookup Address: 1313 Disneyland Dr, Anaheim, CA 92802

List of nearby phone numbers:
[None, '(714) 781-4565', '(714) 781-4565', '(714) 781-4565', '(714) 781-4565', None, '(714) 781-4636', '(714) 781-4000', None, '(888) 758-4389', '(888) 758-4389', None]

Local phone number with the most common first six digits:
(714) 781-4565
```
