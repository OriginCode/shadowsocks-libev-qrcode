#!/usr/bin/python3

import json
import base64
import qrcode
import os
import argparse

parser = argparse.ArgumentParser(description='Generate a QR code of the shadowsocks-libev\'s config.')

parser.add_argument('-c', '--config', type=str, help='Choose a specific config file.')
parser.add_argument('-s', '--save-path', type=str, help='Choose a specific QR code name & path to save.')

group = parser.add_mutually_exclusive_group()
group.add_argument('--ipv4', action='store_true', help='Using IPv4 IP address.')
group.add_argument('--ipv6', action='store_true', help='Using IPv6 IP address.')

args = parser.parse_args()

try:
    f = open(args.config)
except:
    f = open('config.json')
    print('== No specific config file. Using default (./config.json).')

config = json.load(f)
encodestr = config['method'] + ':' + config['password']

if args.ipv4:
    srcstr = "ss://%s@%s:%s#%s" % (base64.b64encode(encodestr.encode()).decode(), config['server'], config['server_port'], 'default')
    print(':: Using IPv4 IP address.')
elif args.ipv6:
    srcstr = "ss://%s@[%s]:%s#%s" % (base64.b64encode(encodestr.encode()).decode(), config['server'], config['server_port'], 'default')
    print(':: Using IPv6 IP address.')
else:
    srcstr = "ss://%s@%s:%s#%s" % (base64.b64encode(encodestr.encode()).decode(), config['server'], config['server_port'], 'default')
    print('== No specific IP address format. Using IPv4 IP address format.')

try:
    qrcode.make(srcstr).save(args.save_path)
    print(':: Image has been saved as %s !' % args.save_path)
except:
    qrcode.make(srcstr).save('image.png')
    print('== No specific image save path. Image has been saved as ./image.png !')

def ifopen():
    answer = input('>> Open the QR Code? [Y/n] ')
    if answer == "n" or answer == "N":
        exit(0)
    elif answer == "y" or answer == "Y":
        try:
            os.system('xdg-open %s' % args.save_path)
        except:
            os.system('xdg-open image.png')
    elif answer == "":
        try:
            os.system('xdg-open %s' % args.save_path)
        except:
            os.system('xdg-open image.png')
    else:
        print('!! Invalid option: %s' % answer)
        ifopen()

ifopen()
