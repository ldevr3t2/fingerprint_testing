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

    temp = base64.b64encode(buf).decode()
    myfile.close() 
    params = {
        'music_buffer': temp
    }
    r = requests.get('http://0.0.0.0:5000/team2/fingerprint', params=params)
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
            ans_list =  eval(ans)
            self.assertTrue(correct[0]['title'] is ans_list[0]['title'])
            

if __name__ == '__main__':
    unittest.main()
