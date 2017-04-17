import connexion
import base64
import os, sys
import json
import hashlib
from acrcloud import *
from acrcloud.recognizer import ACRCloudRecognizer
from acrcloud.recognizer import ACRCloudRecognizeType

from swagger_server.models.info import Info
from datetime import date, datetime
from typing import List, Dict
from six import iteritems
from ..util import deserialize_date, deserialize_datetime


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
        check_answer = {}
        answer = []
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
        answer = [] 
        err = {
            'error': status_msg
        }
        answer.append(err)
        print(answer)
        return err

def fingerprint_get(music_buffer):
    """
    fingerprint_get
    Returns info on the problem
    :param music_buffer: Size of array
    :type music_buffer: str

    :rtype: List[Info]
    """
    #to_byte = music_buffer.encode()
    answer = audio_check(base64.b64decode(music_buffer.encode()))
    print(answer)
    return answer
