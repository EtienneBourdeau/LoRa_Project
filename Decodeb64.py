# !/usr/bin/env python -*- coding: utf-8 -*-

## NEW : V1.3 - Now asks the user which file he wants to analyze.
## NEW : V1.3 - Now supports MicroChip RN2483 In_File.

# This program allows to lay out and decode received messages from Multitech MDOT-EVB-868
# This is a testing program, so it has been concieved for a specific file in a specific "Tests" folder.
# You can change the files to read at line 42 and 57.
# If you want to keep the intermediary file, just comment the final line.
# The main loop analyzes the mid_file line by line and seeks for the pattern corresponding to the wanted data.
# Then, it decodes and calculates GPS coordinates, and write it with SNR, RSSI and time information in the out_file.
# MicroChip RN2483 does not provide GPS coordinates, but provides information about light (un lux, abridged lx)


# ------------------------- #
# Module imports
# ------------------------- #

import base64
import os

# ------------------------- #
# Global Variable
# ------------------------- #

MID_FILE = './mid_file.txt'
LAURENT_FILE = ('./In_Files/laurent/datalaurent.txt')
ETIENNE_FILE = ('./In_Files/etienne/dataetienne.txt')
ALLOWSUITE = False

# ------------------------- #
# Main Program
# ------------------------- #

# User input to determine which file the program must analyse:

answer = input('1 - datalaurent.txt \n2 - dataetienne.txt \nWhich file do you want to analyse ? : ')
test = (int(answer))

# Character replacement from in_file to mid_file
if test == 1:  # Check if datalaurent.txt exists, then lays it out to be read.
    if os.path.isfile(LAURENT_FILE):
        with open('./In_Files/laurent/datalaurent.txt', 'r') as f:
            with open(MID_FILE, 'w') as f2:
                filecontent = f.read()
                filecontent = filecontent.replace(',', '\n').replace(' ', '\n').replace('"', '').replace('{', '')\
                                                        .replace('}', '\n').replace('(null)', '(null) \n')
                f2.write(filecontent)
                print("\nanalyzing 'datalaurent.txt'")
                ALLOWSUITE = True  # When ALLOWSUITE is set to true, the main loop can be run.
    else:
        print("'datalaurent.txt' does not exist or is not in the good folder. Please check.")


elif test == 2:  # Check if dataetienne.txt exists, then lays it out to be read.
    if os.path.isfile(ETIENNE_FILE):
        with open('./In_Files/etienne/dataetienne.txt', 'r') as f:
            with open(MID_FILE, 'w') as f2:
                filecontent = f.read()
                filecontent = filecontent.replace(',', '\n').replace(' ', '\n').replace('"', '').replace('{', '')\
                                                        .replace('}', '\n').replace('(null)', '(null) \n')
                f2.write(filecontent)
                print("\nanalyzing 'dataetienne.txt'")
                ALLOWSUITE = True  # When ALLOWSUITE is set to true, the main loop can be run.
    else:
        print("'dataetienne.txt' does not exist or is not in the good folder. Please check.")

# Checks if the answer is not 1 or 2:
else:
    ALLOWSUITE = False
    print('Please enter a valid answer !')

# MID_FILE analyze, useful info extract, base64 GPS data decode

if ALLOWSUITE:
    with open(MID_FILE, 'r') as f:
        with open('./out_file.txt', 'w') as f2:
                for line in f:
                    if 'lora/' and 'up' in line:
                        for line in f:
                            if 'data' in line:  # Base 64 decoding loop
                                if len(line) > 6:  # Checks if there is code after data:
                                    souschaine = line[5:len(line)]
                                    decoding = base64.b64decode(souschaine)
                                    list1 = list(decoding)
                                    if (len(list1)) == 11:
                                        temp = list1[1]
                                        latitude = (((list1[6] + (list1[5] * 256) + (list1[4] * 256 * 256) + (list1[3] *
                                                                            256 * 256 * 256)) / ((2 ** 31) - 1) * 90))
                                        lat2 = round(latitude, 4)

                                        longitude = ((list1[10] + (list1[9] * 256) + (list1[8] * 256 * 256) + (list1[7]
                                                                            * 256 * 256 * 256)) / ((2 ** 31) - 1) * 180)
                                        lng2 = round(longitude, 4)
                                        result = ('Temperature = ', (str(temp)), '°C', '\n', 'Latitude = ', (str(lat2)),
                                                                      '°', '\n', 'Longitude = ', (str(lng2)), '°', '\n')
                                        result2 = ''.join(result)
                                        f2.write(result2)
                                    elif (len(list1)) < 11 :  # Only works with Microchip RN2483 data:
                                        souschaine = line[5:len(line)]
                                        decoding = base64.b64decode(souschaine)
                                        decodeutf = decoding.decode('utf-8')
                                        kv = decodeutf.split(' ')
                                        temp = (kv[1])[0:3]  # With Microchip data, temperature is always on 3 numbers
                                        result = ('Light = ', kv[0], ' lx', '\n' 'Temperature = ', temp, '°C',
                                        '\n')
                                        result2 = ''.join(result)
                                        f2.write(result2)
                                    elif (len(list1)) > 11:
                                        data = decoding.hex()
                                        res1 = (int((data)[2:4], 16))
                                        calcx = res1 * 0.0625

                                        res2 = (int((data)[4:6], 16))
                                        calcy = res2 * 0.0625

                                        res3 = (int((data)[6:8], 16))
                                        calcz = res3 * 0.0625

                                        res4 = (int((data)[11:16], 16))
                                        calcp = res4 * 0.25

                                        res5 = (int((data)[18:22], 16))

                                        res6 = (int((data)[24:len(data)], 16))
                                        calct = res6 * 0.0625

                                        result = ('Acceleration (x) = ', (str(calcx)), 'g\n', 'Acceleration (y) = ',
                                                  (str(calcy)), 'g\n', 'Acceleration (z) = ', (str(calcz)), 'g\n',
                                                  'Pressure = ', (str(calcp)), 'kPa\n', 'Light = ', (str(res5)), 'lx\n',
                                                  'Temperature = ', (str(calct)), '°C\n')

                                        result2 = ''.join(result)
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

try:
   os.remove(MID_FILE)  # Comment for DEBUG
except FileNotFoundError:
    pass  # Do not generate an error if the program could not run.