#!/usr/bin/env python3

import copy
import datetime
import requests
import os

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

def read_file(url):
    """Get file with all user coordinates and split it into users

    Returns dict with

        dict[username] = string containing coordinate file

    pairs
    """
    data = requests.get(url)
    if data.status_code != 200:  # not successful
        raise IOError
    userdict = {}  # dict that has the multiline string as value for every user
    for section in data.text.split('==>')[1:]:  # split into one file per user, first is empty
        header, text = section.split('\n', 1)  # first line is header
        username = header.split('/')[2]  #  /home/username/public_html/coordinates
        userdict[username] = text
    return userdict

def parse_user(user, text):
    """Create Marker object from coordinates file of the user

    The text should be a single string with newlines
    """
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    marker = Marker()
    marker.user = user
    marker.coords = check_coords(lines[0])
    if len(lines) >= 3:
        marker.color = lines[2]
    if len(lines) >= 2:
        marker.popup = lines[1]
    return marker


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


def main():
    # define filenames
    directory = os.path.dirname(os.path.realpath(__file__))
    markersfile = os.path.join(directory, "markers-users.js")
    logfile = os.path.join(directory, "log_parse.txt")
    templatefile = os.path.join(directory, "template.js")
    coordfile="https://blinkenshell.org/mapdata.txt"

    log = open(logfile, 'w')
    log.write(f"{datetime.datetime.now()}: started script\n")

    log.write("Reading template\n")
    with open(templatefile, 'r') as f:
        template = f.readlines()

    templateheader = ['var users = {\n',
                      '  "type": "FeatureCollection",\n',
                      '  "features": [\n'
                      ]
    templatefooter = ['  ]\n',
                      '};'
                      ]

    log.write("Opening markers file and writing header\n")
    f = open(markersfile, 'w')
    f.writelines(templateheader)

    user_json = copy.deepcopy(template)
    user_counter = 0

    userdict = read_file(coordfile)
    log.write(f"Found {len(userdict)} blinkenshellers in file, starting to parse their texts\n\n")
    for user, text in userdict.items():
        try:
            marker = parse_user(user, text)
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
    log.write(f"{datetime.datetime.now()}: finished script\n")
    log.close()


if __name__ == '__main__':
    main()
