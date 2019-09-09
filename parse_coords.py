#!/usr/bin/env python3

import os
import urllib.request

class Marker:
    """Stores the information of a user"""
    def __init__(self):
        self.user = None
        self.coords = [0.000,0.000]
        self.popup = None
        self.color = None


def check_coords(line):
    """Check if coordinates were given in correct way"""
    coords = line.split(',') # must comma seperated
    coords = [float(coord) for coord in coords]
    if len(coords) != 2:
        raise ValueError("Must be 2 values for coordinates")
    if abs(coords[0] > 180):
        raise ValueError("Longitude can't be larger than 180")
    if abs(coords[1] > 90):
        raise ValueError("Latitude can't be larger than 120")
    return coords # switch lonlat to latlon to make it user friendly?


def parse_user(user, filename):
    urlpattern = "http://" + user + ".blinkenshell.org/" + filename
    lines = []
    with urllib.request.urlopen(urlpattern) as f:
        lines = [line.decode().strip() for line in f.readlines()]
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


def change_template(marker, template):
    template[4] = f'          {marker.coords[0]},\n'
    template[5] = f'          {marker.coords[1]}\n'
    template[10] = f'        "user": "{marker.user}",\n'
    if marker.color:
        template[12] = f'        "color": "{marker.color}"\n'
    else:
        del template[12]
    if marker.popup:
        template[11] = f'        "popupContent": "{marker.popup}",\n'
    else:
        del template[11]
    return template


if __name__ == '__main__':
    # users = os.listdir("/home/")
    users = ["pbnoxious"]

    templateheader = ['var users = {\n',
                      '  "type": "FeatureCollection",\n',
                      '  "features": [\n'
                      ]
    templatefooter = ['  ]\n',
                      '};'
                      ]

    template = get_template()

    f = open('testmarkers', 'w')
    f.writelines(templateheader)

    all_user_templates = []
    all_user_templates.append(templateheader)

    for user in users:
        try:
            marker = parse_user(user, "coordinates")
        except PermissionError:
            print(f"Wrong permissions for user {user}")
        except IOError:
            print(f"File of user {user} not readable")
        except ValueError:
            pass
        change_template(marker, template)
        f.writelines(template)

    f.writelines(templatefooter)
    f.close()

    # later: use f.seek to only append the changed ones? how to search for the only changed ones?
