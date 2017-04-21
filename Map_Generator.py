# !/usr/bin/env python -*- coding: utf-8 -*-

# Use ONLY after decodeb64.py, since you will need out_file.txt it creates.
# This code is NOT portable, you need to install the folium module first.
# This program creates a map in html in the same folder from where you execute this program.
# The map contains markers. Their position corresponds to GPS coordinates from out_file.txt. If you click on it,
# you will have the other information written on out_file.txt

# NEW v1.4 : Now automatically centers the map on the first latitude and longitude found.

# ------------------------- #
#     Module imports
# ------------------------- #

import folium  # WARNING : Folium is not integrated to Python. Please install it before running this code.

# ------------------------- #
#     Global Variable
# ------------------------- #

file = './out_file.txt' # Name of file to read
LAT = 'Latitude'
LNG = 'Longitude'
TMP = 'Temperature'
LSNR = 'Signal to Noise Ratio'
RSSI = 'Received Signal Strength Indicator (dBm)'
DAT = 'Date'

# ------------------------- #
#      Map Creation
# ------------------------- #

with open('./out_file.txt', 'r') as f:  # Finds the first latitude and longitude in out_file.
    lat1 = None
    lng1 = None
    for line in f:  # Analyzes out_file line by line
        kv = line.split(' = ')  # kv = Key Value. kv[0] = Key (text before '='). kv[1] = Value (values after '=')
        if kv[0] == LAT:
            value = kv[1].strip('°\n')
            lat1 = float(value)
        elif kv[0] == LNG:
            value = kv[1].strip('°\n')
            lng1 = float(value)
            break

coord = (lat1, lng1)
mymap = folium.Map(location=coord, zoom_start=16)

# coord_cezeaux = (45.7618, 3.1094)
# cez = folium.Map(location=coord_cezeaux, zoom_start=16)


# ------------------------- #
#      Main Program
# ------------------------- #
try:
    with open(file, 'r') as f:
        lat = None
        lng = None
        tmp = None  # Initializing all values to False, so you can check their presence later.
        rssi = None
        dat = None
        lsnr = None
        creamap = None
        for line in f:
            kv = line.split(' = ')  # Creates a table, splitting columns from '=': 1st element is the key, 2nd is the value.
            if kv[0] == TMP:  # Checks if each line contains the wanted pattern(patterns are set in Global Variables above).
                value = kv[1].strip('°C\n')
                tmp = float(value)
            elif kv[0] == LAT:
                value = kv[1].strip('°\n')
                lat = float(value)
            elif kv[0] == LNG:
                value = kv[1].strip('°\n')
                lng = float(value)
            elif kv[0] == LSNR:
                value = kv[1].strip('\n')
                lsnr = float(value)
            elif kv[0] == RSSI:
                value = kv[1].strip('\n')
                rssi = int(value)
            elif kv[0] == DAT:
                dat = kv[1].strip('\n')
            if lat and rssi and lng and tmp and lsnr and dat:  # When all patterns are found :
                # Laying out of the marker
                markerpopup = ('Temperature = ', str(tmp), '°C || ', 'Latitude = ', str(lat), '° || ', 'Longitude = ',
                               str(lng), '° || ', 'Signal to Noise Ratio (SNR) = ', str(lsnr), ' || ',
                               ' Received Signal Strength Indicator (dBm) = ', str(rssi), ' ||', ' Date = ', str(dat))
                markerpopup2 = ''.join(markerpopup)
                folium.Marker([lat, lng], popup=markerpopup2).add_to(mymap)  # Creation of the marker
                lat = None
                lng = None  # Set back latitude and longitude to False, else they won't be found on next iteration.
                creamap = True

# ------------------------- #
#        Map Save
# ------------------------- #

    if creamap == True:
        mymap.save('./map.html')  # Save map with markers on it
    else:
        print('Unable to generate a map. Please check latitudes and longitudes in out_file.')
        print("If you did not use Multitech Mdot data with Decodeb64.py, you may not have GPS data.")
        creamap = False

except FileNotFoundError:
    print('out_file.txt is missing. Please run Decodeb64.py and check out_file.txt is created.')
