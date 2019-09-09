#!/usr/bin/env python3

import os

class Marker:
    def __init__(self):
        self.user = None
        self.coords = [0.000,0.000]
        self.popup = None
        self.color = None


def check_coords(line):
    coords = line.split(',') # must comma seperated
    if len(coords != 2):
        raise ValueError("Must be 2 values for coordinates")
    if abs(coords[0] > 180):
        raise ValueError("Longitude can't be larger than 180")
    if abs(coords[1] > 90):
        raise ValueError("Latitude can't be larger than 120")
    return coords # switch lonlat to latlon to make it user friendly?


def parse_user(user):
    filepattern = "coordinates"
    filename = "/home/" + user + "/public_html/" + filepattern

    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line]
    marker = Marker()
    marker.user = user
    marker.coords = check_coords(lines[0])
    marker.popup = lines[1]
    marker.color = lines[2]
    return marker


def get_template():
    with open("template.js", 'r') as f:
        lines = f.readlines()
    return lines


if __name__ == '__main__':
    users = os.listdir("/home/")
    template = get_template()

    for user in users:
        try:
            marker = parse_user(user)
        except PermissionError:
            print("Wrong permissions for user {}".format(user))
        except IOError:
            print("File of user {} not readable".format(user))
        except ValueError:
            pass
        change_template(marker, template)

def change_template(marker, template):
    template[4] = '          {},\n'.format(marker.coords[0])
    template[5] = '          {},\n'.format(marker.coords[1])
    template[10] = '        "user": "{}",\n'.format(marker.user)
    if marker.color:
        template[12] = '        "color": "{}"\n'.format(marker.color)
    else:
        del template[12]
    if marker.popup:
        template[11] = '        "popupContent": "{}",\n'.format(marker.popup)
    else:
        del template[11]
    return template
