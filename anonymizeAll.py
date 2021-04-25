import os
import re
from pathlib import Path
#import functions that will create regex patterns and anonymize text strings
from definitions import *

#Create 3 regex patterns out of 3 list of names: 'firstnames.txt', 'lastnames.txt' and 'placenames.txt'.
#Note that complete names (ex. Alexis) MUST PRECEDE partial names (ex. Ale) for this to work!!!

with open('firstnames.txt', 'r') as file:
    firstnames = file.read()
    firstnameslist = firstnames.split()

firstregex = '|'.join([pattern(name) for name in firstnameslist])

with open('lastnames.txt', 'r') as file:
    lastnames = file.read()
    lastnameslist = lastnames.split()

lastregex = '|'.join([pattern(name) for name in lastnameslist])

with open('placenames.txt', 'r') as file:
    placenames = file.read()
    placenameslist = placenames.split()

placeregex = '|'.join([pattern(name) for name in placenameslist])


#Anonymize a folder of files using these three regular expressions.
#Note that the folder MUST be located in the same directory as this script.
#Place the resulting anonymized files into a new folder inside the one you gave.

indirectory = input('Enter the name of the folder you want to anonymize:\n')
outdirectoryname = f'{indirectory}-anonymized'
outdirectory = Path(f'{indirectory}/{outdirectoryname}')
outdirectory.mkdir(exist_ok=True)

with os.scandir(indirectory) as infiles:
    for infile in infiles:
        if not infile.name.startswith('.') and infile.is_file(): #exclude all invisible files and non-files
            inpath = f'{indirectory}/{infile.name}'
            print(inpath, 'will be anonymized')

            with open(inpath, 'r') as file:
                lines = file.readlines()

            outfilename = re.sub('\.', '-anonymized.', infile.name)
            outfilepath = f'{outdirectory}/{outfilename}'

            with open(outfilepath, 'w') as outfile:
                for line in lines:
                    anonymousfirst = anonymize(line, firstregex, 'Firstname')
                    anonymouslast = anonymize(anonymousfirst, lastregex, 'Lastname')
                    anonymousline = anonymize(anonymouslast, placeregex, 'Placename')
                    outfile.write(anonymousline)

            print(f'{outfilepath} has been created')