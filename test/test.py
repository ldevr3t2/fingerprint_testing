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
    
    headers = {
	"Accept": "application/json", \
	"Content-Type": "application/json"
    }

    temp = base64.b64encode(buf).decode()
    #print(type(base64.b64encode(buf)))
    #print(base64.b64encode(buf))
    myfile.close() 
    data = {
        'music_buffer': temp
    }
    r = requests.post('http://0.0.0.0:5000/team2/fingerprint',   \
            data=json.dumps(data), headers=headers)
    
    return r.text

class Test(unittest.TestCase):
        def setUp(self):
                pass
        '''
        test non exist music
        '''
        def testNonExist(self):
            ans = getbuffer('nonexist.mp3')
            correct = {
                    'error' : "No result"
            }
            ans_dict = json.loads(ans)
            self.assertEqual(correct['error'], ans_dict['error'])

        '''
        test invalid file
        '''
        def testInvalidFile(self):
            ans = getbuffer('invalid.txt')
            correct = {
                    'error' : "audio error"
            }
            ans_dict = json.loads(ans)
            self.assertEqual(correct['error'], ans_dict['error'])


        '''
        test exist music
        '''
        def testExist(self):
            ans = getbuffer('10s.mp3')
            correct = [
                {
                    "artists" : [
                        {
                            "name": "Maksim Mrvica"
                        }    
                    ],
                    "title": "Wonderland"
                } 
            ]
            ans_list = json.loads(ans)
            self.assertEqual(correct[0]['title'], ans_list['title'])
            

if __name__ == '__main__':
    unittest.main()
