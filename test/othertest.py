import os, sys
import json
import hashlib
import requests
import base64
import unittest

def getbuffer(filename):
    myfile = open(filename, 'rb')
    buf = myfile.read()
    if filename.endswith('.wav'):
        buf = buf[1024000:192000+1024001]

    # buf type - bytes
    # 1. using base64 encode buf data
    # 2. decode previous encoded data
    # 3. send get request
    #
    # param format
    # params = {
    #   'music_buffer': buf
    # }

    temp = base64.b64encode(buf).decode()
    #print(type(base64.b64encode(buf)))
    #print(base64.b64encode(buf))
    myfile.close() 
    params = {
        'music_buffer': temp
    }
    r = requests.get('http://0.0.0.0:5000/team2/fingerprint', params=params)
    return r.text

ans = getbuffer('nonexist.mp3')
print(ans)
