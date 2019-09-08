#!/usr/bin/env python3


def check_coords(line):
    coords = line.split(,) # must comma seperated
    if len(coords == 2):
        raise ValueError('Must be 2 values for coordinates')


def parse_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line]
    coords = check_coords(lines[0])


for filename in filelist:
    try:
        parse_file(filename)
    except:
        IOError: 
            print("File {} not readable".format(filename))
            pass
        ValueError:
            pass
            

        
