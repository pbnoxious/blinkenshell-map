#!/usr/bin/env python3

import os
import copy

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
    if abs(coords[0] > 90):
        raise ValueError("Latitude can't be larger than 90")
    if abs(coords[1] > 180):
        raise ValueError("Longitude can't be larger than 180")
    return coords


def parse_user(user, filename):
    """Reads file of user and returns Marker with info"""
    urlpattern = "http://" + user + ".blinkenshell.org/" + filename
    lines = os.popen(f"curl -s {urlpattern}").readlines()
    if len(lines) == 7 or len(lines) == 0:
        raise IOError
    lines = [line.strip() for line in lines if line]
    marker = Marker()
    marker.user = user
    marker.coords = check_coords(lines[0])
    if len(lines) >= 3:
        marker.color = lines[2]
    if len(lines) >= 2:
        marker.popup = lines[1]
    return marker


def get_template():
    with open("template.js", 'r') as f:
        lines = f.readlines()
    return lines


#def read_old_markers(filename):
#    with open(filename, 'r') as f:
#        lines = f.readlines()
#    lines = lines[3:-2] # remove template header and footer
#    line_iter= iter(lines) 
#    for line in line_iter:
#        if line = f'"coordinates": ['
#    marker = Marker()


def change_template(marker, template):
    """Enter marker information into geojson template"""
    fetch_new = False
    template[4] = f'          {marker.coords[1]},\n' # switch latlon to lonlat
    template[5] = f'          {marker.coords[0]}\n'  # because of geojson
    template[10] = f'        "user": "{marker.user}",\n'
    if marker.color:
        template[12] = f'        "color": "{marker.color}"\n'
    else:
        del template[12]
        fetch_new = True
    if marker.popup:
        template[11] = f'        "popupContent": "{marker.popup}",\n'
    else:
        del template[11]
        fetch_new = True
    return (template, fetch_new)


if __name__ == '__main__':
    markersfile = "markers-users.js"
    logfile = "log_parse.txt"
    users = os.listdir("/home/")
    #users = ["pbnoxious", "djm", "Nistur", "luke", "derkirche", "esselfe", "peron", "period"]

    templateheader = ['var users = {\n',
                      '  "type": "FeatureCollection",\n',
                      '  "features": [\n'
                      ]
    templatefooter = ['  ]\n',
                      '};'
                      ]

    template = get_template()

    log = open(logfile, 'w')
    f = open(markersfile, 'w')
    f.writelines(templateheader)

    user_json = copy.deepcopy(template)
    user_counter = 0

    for user in users:
        try:
            marker = parse_user(user, "coordinates")
        except IOError:
            log.write(f"File of user {user} not found\n")
            continue
        except ValueError as e:
            log.write(f"File of user {user} is not correct: {e}\n")
            continue
        user_json, fetch_new = change_template(marker, user_json)
        f.writelines(user_json)
        user_counter += 1
        if fetch_new:
            user_json = copy.deepcopy(template)
    log.write(f"\n{user_counter} blinkenshellers added to map successfully!\n")

    f.writelines(templatefooter)
    f.close()
    log.close()
