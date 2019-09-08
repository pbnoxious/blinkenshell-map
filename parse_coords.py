#!/usr/bin/env python3

class Marker:
    def __init__(self):
        self.user = "Anonymous"
        self.coords = [0.000,0.000]
        self.popup = None
        self.color = None


def get_filelist():
    filepattern = "coordinates"
    # how to best get a list of all public_html directories?
    filelist = filepattern
    return filelist


def check_coords(line):
    coords = line.split(',') # must comma seperated
    if len(coords == 2):
        raise ValueError("Must be 2 values for coordinates")
    if abs(coords[0] > 180):
        raise ValueError("Longitude can't be larger than 180")
    if abs(coords[1] > 90):
        raise ValueError("Latitude can't be larger than 120")
    return coords # switch lonlat to latlon to make it user friendly?


def parse_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line]
    marker = Marker()
    marker.coords = check_coords(lines[0])
    marker.popup = lines[1]
    marker.color = lines[2]
    return marker




if __name__ == '__main__':
    filelist = get_filelist()
    for filename in filelist:
        try:
            parse_file(filename)
        except IOError:
            print("File {} not readable".format(filename))
        except ValueError:
            pass
