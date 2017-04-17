import os, sys
import json
import hashlib
from pymongo import *
from acrcloud import acrcloud_extr_tool
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType

global mongo_client
global mongo_db
global mongo_collection
global mongo_post 

'''
    audio identifier
'''
audio_identifier_host = 'identify-us-west-2.acrcloud.com'
audio_identifier_access_key = '752fc37a314b655ac215d58d45943a0c'
audio_identifier_access_secret = 'Y4w6rRa86YdrjlL1oxeRLqLgryPWyzMeoYmTTWe1'

def audio_check(file_buffer):
    config = {
        'host': audio_identifier_host,  
        'access_key': audio_identifier_access_key,
        'access_secret': audio_identifier_access_secret,
        'recognize_type': ACRCloudRecognizeType.ACR_OPT_REC_AUDIO, 
        'debug':False,
        'timeout':10 # seconds
    }
    
    re = ACRCloudRecognizer(config)
    res_str = re.recognize_by_filebuffer(file_buffer, 0, 10)
    res_dict = json.loads(res_str)
    
    status_code = res_dict["status"]["code"]
    if status_code == 0:
        # TO DO 
        # create answer payload
        metadata =res_dict["metadata"]
        metadata_music_list = metadata["music"]
        answer = []
        check_answer = {}
        for i in range (0, len(metadata_music_list)):
            title = metadata_music_list[i]["title"]
            artists = metadata_music_list[i]["artists"] 
            song = {
                'title': title,
                'artists': artists
            }
            hashed_val = hashlib.sha1(json.dumps(song,  \
                        sort_keys=True).encode()).hexdigest()
            if check_answer.get(hashed_val) == None:
                check_answer[hashed_val] = i
                answer.append(song)
        return answer
    else:
        status_msg = res_dict["status"]["msg"]

        print(status_msg)
        return status_msg
        

def getbuffer(filename):
    buf = open(filename, 'rb').read()
    print(type(buf))
    if filename.endswith('.wav'):
        buf = buf[1024000:192000+1024001]
    fingerprint =   \
        acrcloud_extr_tool.create_humming_fingerprint_by_filebuffer(buf,    \
            0, 10)
    print(type(fingerprnt))
    answer = audio_check(buf)
    print(answer)

if __name__ == "__main__":

    getbuffer(sys.argv[1])
