# !/usr/bin/env python -*- coding: utf-8 -*-

# ------------------------- #
# Module imports
# ------------------------- #

import folium

# ------------------------- #
# Map Creation
# ------------------------- #

coord_cezeaux = (45.7618, 3.1094)
cez = folium.Map(location=coord_cezeaux, zoom_start=17)

# ------------------------- #
# Global Variable
# ------------------------- #

file = './out_file.txt' # Name of file to read
LAT = 'latitude'
LNG = 'longitude'
TMP = 'température'
LSNR = 'Rapport Signal / Bruit'
RSSI = 'Puissance du signal (en dBm)'
DAT = 'Date'

# ------------------------- #
# Main Program
# ------------------------- #

with open(file, 'r') as f:
    lat = None
    lng = None
    tmp = None
    rssi = None
    dat = None
    lsnr = None
    for line in f:
        kv = line.split(' = ')
        if kv[0] == TMP:
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
        if lat and rssi and lng and tmp and lsnr and dat:
            # msg = "lat: {}, long: {}".format(lat, long)
            markerpopup = ('température = ', str(tmp), '°C || ', 'latitude = ', str(lat), '° || ', 'longitude = ',
                           str(lng), '° || ', 'Rapport Signal / Bruit = ', str(lsnr), ' || ',
                           ' Puissance du Signal (en dBm) = ', str(rssi), ' ||', ' Date = ', str(dat))
            markerpopup2 = ''.join(markerpopup)
            folium.Marker([lat, lng], popup=markerpopup2).add_to(cez)
            lat = None
            lng = None

# ------------------------- #
# Map Save
# ------------------------- #

cez.save('./map.html')  # Save map with markers on it
