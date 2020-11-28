
'''
@author: frederic rivollier

'''

import re, sys, os
import json, struct
import numpy as np

from .core import text_to_dict

import logging
logging.addLevelName(5,"VERBOSE")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pvsyst')

from pprint import pprint, pformat

# read OND file and return dict
def ond_to_inverter_param(path):

    # group keys of PVSYST 6.7.6
    # key is the start value to identify
    # vlaue is the dict key to be used


    ond_sections ={'PVObject_': 'pvGInverter',
                'PVObject_Commercial': 'pvCommercial',
                'Converter': 'TConverter',
                'Remarks, Count': 'Remarks',
                'ProfilPIOV1': 'ProfilPIOV1',
                'ProfilPIOV2': 'ProfilPIOV2',
                'ProfilPIOV3': 'ProfilPIOV3'}

    #open file
    with open(path, mode='r', encoding='utf-8-sig') as file: # utf-8-sig to fix u'\ufeff' BOM issue on certain OS
        raw = file.read()
        if raw[:3] == "ï»¿": # this is utf-8-BOM
            raw = raw[3:] #remove BOM

    #parse text file to nested dict based on pan_keys
    data = text_to_dict(raw, ond_sections)
    logger.debug(pformat(data))


    return data


def _test():

    ond_file = 'refSMA_Central_2750.OND'
    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/', ond_file)


    logger.setLevel(10)  # 5 for Verbose 10 for Debug

    m = ond_to_inverter_param(path)
