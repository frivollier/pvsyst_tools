'''
@author: frederic rivollier
    2018.10.28 Initial draft
    2019.03.23 Clean up

Pre-requisites:

Overview:

Revision history
    0.0.1:  Initial stable release
    0.1.0:  Simplifyed logic
'''

import re, sys, os
import json, struct
import numpy as np

import logging
logging.addLevelName(5,"VERBOSE")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pvsyst_io')

from pprint import pprint, pformat

#parse indented text and yield level, parent and value
def _parse_tree(lines):
    """
    Parse an indented outline into (level, name, parent) tuples.  Each level
    of indentation is 2 spaces.
    """
    regex = re.compile(r'^(?P<indent>(?: {2})*)(?P<name>\S.*)')
    stack = []
    for line in lines:
        match = regex.match(line)
        if not match:
            continue #skip last line or empty lines
            #raise ValueError('Indentation not a multiple of 2 spaces: "{0}"'.format(line))
        level = len(match.group('indent')) // 2
        if level > len(stack):
            raise ValueError('Indentation too deep: "{0}"'.format(line))
        stack[level:] = [match.group('name')]
        yield level, match.group('name'), (stack[level - 1] if level else None)

#for PVSYST files parsing to DICT. Takes list of group keys and return dict
def _text_to_dict(m, sections):
    data = dict()
    levels_temp = [None]*10  # temporary array to store current keys tree

    # parse each line of m string (PAN file)
    for level, name, parent in _parse_tree(m.split('\n')):
        #try for line with no = sign i.e. End of we will continue
        try:
            key = re.split('=',name)[0]
            value = re.split('=',name)[1]
            logger.log(5, '{}{}:{} [l{},p{}]'.format(' ' * (2 * level), key, value, level, parent))
        except:
            continue

        # Create group keys for current level
        # check if key if in sections dict
        group = [v for k, v in sections.items() if key == k]
        if group:
            if level == 0:
                data[group[0]] = dict()
                levels_temp[0] = data[group[0]]
                logger.log(5, 'set levels_temp[0] to data[{}]'.format(name))

            else:
                levels_temp[level - 1][group[0]] = dict()
                levels_temp[level] = levels_temp[level - 1][group[0]]
                logger.log(5, 'set levels_temp[{}] to data[{}]'.format(level, group[0]))

        else:
            levels_temp[level-1][key] = value


    return data

# read PAN file and return dict of module paramters for PVLIB
def pan_to_module_param(path):

    # group keys of PVSYST 6.7.6
    # key is the start value to identify
    # vlaue is the dict key to be used
    pan_sections ={'PVObject_': 'pvModule',
                'PVObject_Commercial': 'pvCommercial',
                'PVObject_IAM': 'pvIAM',
                'IAMProfile': 'TCubicProfile',
                'Remarks, Count': 'Remarks',
                'OperPoints, list of': 'tOperPoint'}

    #open file
    with open(path,'r') as file:
        raw = file.read()

    #parse text file to nested dict based on pan_keys
    data = _text_to_dict(raw, pan_sections)
    logger.debug(pformat(data))

    m = {}
    m['manufacturer'] = (data['pvModule']['pvCommercial']['Manufacturer'])
    m['module_name'] = (data['pvModule']['pvCommercial']['Model'])
    m['Technol'] = (data['pvModule']['Technol'])

    m['CellsInS'] = int(data['pvModule']['NCelS'])
    m['CellsInP'] = int(data['pvModule']['NCelP'])
    m['GRef'] = float(data['pvModule']['GRef'])
    m['TRef'] = float(data['pvModule']['TRef'])
    m['Pmpp'] = float(data['pvModule']['PNom'])
    m['Isc'] = float(data['pvModule']['Isc'])
    m['Voc'] = float(data['pvModule']['Voc'])
    m['Impp'] = float(data['pvModule']['Imp'])
    m['Vmpp'] = float(data['pvModule']['Vmp'])

    m['mIsc_percent'] = (float(data['pvModule']['muISC'])/1000/m['Isc'])*100 #PAN stored in mA/C,convert to %/C
    m['mVoc_percent'] = (float(data['pvModule']['muVocSpec'])/1000/m['Voc'])*100 # PAN stored in mV/C, convert to %/C

    m['mIsc'] = float(data['pvModule']['muISC'])/1000  # convert to A/C
    m['mVoc'] = float(data['pvModule']['muVocSpec'])/1000  # convert to V/C

    m['mPmpp'] = float(data['pvModule']['muPmpReq'])
    m['Rshunt'] = float(data['pvModule']['RShunt'])
    m['Rsh 0'] = float(data['pvModule']['Rp_0'])
    m['Rshexp'] = float(data['pvModule']['Rp_Exp'])
    m['Rserie'] = float(data['pvModule']['RSerie'])
    m['Gamma'] = float(data['pvModule']['Gamma'])
    m['muGamma'] = float(data['pvModule']['muGamma'])

    # IAM profile to ndarray
    try:
        if data['pvModule']['pvIAM']['IAMMode'] == 'UserProfile':
            points = int(data['pvModule']['pvIAM']['TCubicProfile']['NPtsEff'])
            x = []
            y = []
            for n in range(points):
                v = data['pvModule']['pvIAM']['TCubicProfile']['Point_{}'.format(n+1)]
                v = v.split(',')
                x.append(float(v[0]))
                y.append(float(v[1]))
            m['IAM'] = np.array([x,y])
    except Exception as e:
        logger.warning('IAM profile not found')
        logger.log(5, e)
        m['IAM'] = None




    #constants
    k = 1.38064852e-23 #Boltzmann’s constant (J/K)
    kelvin0 = 273.15
    q = 1.60217662e-19 # charge of an electron (coulombs)
    GRef = 1000
    Tc = 25 + kelvin0 #Deg Kelvin

    #solve IoRef for Voc
    I = 0
    V = m['Voc']
    IoRefVoc = -((I+(V + I*m['Rserie'])/\
                m['Rshunt'])-m['Isc'])/\
                (np.exp(q*(V+I*m['Rserie'])/\
                (m['CellsInS']*m['Gamma']*k*Tc))-1)

    #solve IoRef for Pmax
    I = m['Impp']
    V = m['Vmpp']
    IoRefPmp = -((I+(V + I*m['Rserie'])/\
                m['Rshunt'])-m['Isc'])/\
                (np.exp(q*(V+I*m['Rserie'])/\
                (m['CellsInS']*m['Gamma']*k*Tc))-1)

    # pvlib mpodule paramters
    m['gamma_ref'] = m['Gamma']
    m['mu_gamma'] = m['muGamma']
    m['I_L_ref'] = m['Isc']
    m['I_o_ref'] = IoRefPmp  # Using Pmp curve fitting, TODO; check CASSYS
    m['EgRef'] = 1.121  # The energy bandgap at reference temperature in units of eV
    m['R_sh_ref'] = m['Rshunt']
    m['R_sh_0'] = m['Rsh 0']
    m['R_s'] = m['Rserie']
    m['R_sh_exp'] = m['Rshexp']
    m['cells_in_series'] = m['CellsInS']
    m['alpha_sc'] = m['mIsc']  # A/C

    return m
