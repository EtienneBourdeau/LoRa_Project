# !/usr/bin/env python -*- coding: utf-8 -*-

# This program allows to lay out and decode received messages from Multitech MDOT-EVB-868
# This is a testing program, so it has been concieved for a specific file in a specific "Tests" folder.
# You can change the file to read at line 29.
# If you want to keep the intermediary file, just comment the final line.
# The main loop analyzes the mid_file line by line and seeks for the pattern corresponding to the wanted data.
# Then, it decodes and calculates GPS coordinates, and write it with SNR, RSSI and time information in the out_file.

# ------------------------- #
# Module imports
# ------------------------- #

import base64
import os  # useful only when commenting the last line

# ------------------------- #
# Global Variable
# ------------------------- #

mid_file = './mid_file.txt'

# ------------------------- #
# Main Program
# ------------------------- #

# Character replacement from in_file to mid_file

with open('./Tests/data_6mars_cezeaux.txt', 'r') as f:
    with open(mid_file, 'w') as f2:
        filedata = f.read()
        filedata = filedata.replace(',', '\n').replace(' ', '\n').replace('"', '').replace('{', '').replace('}', '\n')\
            .replace('(null)', '(null) \n')
        f2.write(filedata)

# Mid_file analyze, useful info extract, base64 GPS data decode

with open(mid_file, 'r') as f:
    with open('./out_file.txt', 'w') as f2:
            for line in f:
                if 'lora/' and 'up' in line:
                    for line in f:
                        if 'data' in line:  # Base 64 decoding loop
                            souschaine = line[5:len(line)]
                            decodage = base64.b64decode(souschaine)
                            liste = list(decodage)
                            temp = liste[1]
                            latitude = (((liste[6] + (liste[5] * 256) + (liste[4] * 256 * 256) + (liste[3] * 256 * 256 *
                                                                256)) / ((2 ** 31) - 1) * 90))
                            lat2 = round(latitude, 4)

                            longitude = ((liste[10] + (liste[9] * 256) + (liste[8] * 256 * 256) + (liste[7] * 256 * 256
                                                                * 256)) / ((2 ** 31) - 1) * 180)
                            lng2 = round(longitude, 4)
                            resultat = ('Temperature = ', (str(temp)), '°C', '\n', 'Latitude = ', (str(lat2)),
                                        '°', '\n', 'Longitude = ', (str(lng2)), '°', '\n')
                            result2 = ''.join(resultat)
                            f2.write(result2)
                        elif 'lsnr:' in line:  # Signal to Noise Ratio retrieving
                            lsnr = ('Signal to Noise Ratio = ', line[5:len(line)])
                            lsnr2 = ''.join(lsnr)
                            f2.write(lsnr2)
                        elif 'rssi:' in line:  # Received Signal Strength Information retreiving
                            rssi = ('Received Signal Strength Indicator (dBm) = ', line[5:len(line)])
                            rssi2 = ''.join(rssi)
                            f2.write(rssi2)
                        elif 'timestamp:' in line:  # Time information formating + laying out
                            year = line[10:14]
                            month = line[15:17]
                            day = line[18:20]
                            hour = line[21:23]
                            minutes = line[24:26]
                            seconds = line[27:29]
                            time = ('Date = ', month, '-', day, '-', year, ', at ', hour, 'h', minutes, ' (',
                                    seconds, ' seconds)', '\n', '\n')
                            time2 = ''.join(time)
                            f2.write(time2)
                        if 'tmst:' in line:  # If end of packet is met, break
                            break

os.remove(mid_file)  # Comment for DEBUG
