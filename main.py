#!/usr/bin/python3

import json
import base64
import qrcode
import os
import sys

try:
    f = open(sys.argv[1])
except:
    f = open("config.json")
    print('No specific config file. Using default (./config.json).')

config = json.load(f)
encodestr = config['method'] + ':' + config['password']
srcstr = "ss://%s@%s:%s#%s" % (base64.b64encode(encodestr.encode()).decode(), config['server'], config['server_port'], 'default')
qrcode.make(srcstr).save('image.png')

print('Image has been saved as ./image.png !')
answer = input('Open the QR Code? [Y/n] ')

if answer == "n" or answer == "N":
    exit(0)
elif answer == "y" or answer == "Y":
    os.system('xdg-open image.png')
elif answer == "":
    os.system('xdg-open image.png')
else:
    print('Invalid option: %s' % answer)
