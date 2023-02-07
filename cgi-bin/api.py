#!/usr/bin/python3

print("Content-type: application/json\n\n")

import urllib.request
page = urllib.request.urlopen('https://www.giantbomb.com/api/game/3030-4725/?api_key=9f5f504612747bac723f6776a7e63514959350e2&format=json')
print(page.read().decode('ascii'))
