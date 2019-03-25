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
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)


'''
# PVSYST one diode module paramaeters
#I=Iph-Io*(np.exp(q*(V+I*Rs)/(Ncs·Gamma·k·Tc))-1)-(V + I*Rs)/Rsh

#PVSYST one diode equation
http://files.pvsyst.com/help/index.html?pvcell_reversechar.htm

I  =  Iph  -   Io  [ exp  (q · (V+I·Rs) / ( Ncs·Gamma·k·Tc) ) - 1 ]    -    (V + I·Rs) / Rsh

with :
I        =        Current supplied by the module  [A].
V        =        Voltage at the terminals of the module  [V].
Iph        =        Photocurrent [A], proportional to the irradiance G,  with a correction as function of  Tc  (see below).
ID        =        Diode current, is the product   Io  ·  [exp(     ) -1].
Io        =        inverse saturation current, depending on the temperature [A]  (see expression below).
Rs        =        Series resistance [ohm].
Rsh        =        Shunt resistance [ohm].
q        =        Charge of the electron  =  1.602·E-19 Coulomb
k        =        Bolzmann's constant =  1.381 E-23  J/K.
Gamma=          Diode quality factor, normally between 1 and 2
Ncs        =        Number of cells in series.
Tc        =        Effective temperature of the cells [Kelvin]


PVLIB Parameters
    ----------
    effective_irradiance : numeric
        The irradiance (W/m2) that is converted to photocurrent.
    temp_cell : numeric
        The average cell temperature of cells within a module in C.
    alpha_sc : float
        The short-circuit current temperature coefficient of the
        module in units of A/C.
    gamma_ref : float
        The diode ideality factor
    mu_gamma : float
        The temperature coefficient for the diode ideality factor, 1/K
    I_L_ref : float
        The light-generated current (or photocurrent) at reference conditions,
        in amperes.
    I_o_ref : float
        The dark or diode reverse saturation current at reference conditions,
        in amperes.
    R_sh_ref : float
        The shunt resistance at reference conditions, in ohms.
    R_sh_0 : float
        The shunt resistance at zero irradiance conditions, in ohms.
    R_s : float
        The series resistance at reference conditions, in ohms.
    cells_in_series : integer
        The number of cells connected in series.
    R_sh_exp : float
        The exponent in the equation for shunt resistance, unitless. Defaults
        to 5.5.
    EgRef : float
        The energy bandgap at reference temperature in units of eV.
        1.121 eV for crystalline silicon. EgRef must be >0.
    irrad_ref : float (optional, default=1000)
        Reference irradiance in W/m^2.
    temp_ref : float (optional, default=25)
        Reference cell temperature in C.
'''

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
def _text_to_dict(m, group_keys):
    data = dict()
    levels_temp = [None]*10  # temporary array to store current keys tree

    # parse each line of m string (PAN file)
    for level, name, parent in _parse_tree(m.split('\n')):
        #try for line with no = sign i.e. End of we will continue
        try:
            key = re.split('=',name)[0]
            value = re.split('=',name)[1]
            logger.debug('{}{}:{} [l{},p{}]'.format(' ' * (2 * level), key, value, level, parent))
        except:
            continue

        # Create group keys for current level
        if name.startswith(tuple(group_keys)):
            if level == 0:
                data[name] = dict()
                levels_temp[0] = data[name]

                logger.debug('set levels_temp[0] to data[{}]'.format(name))
                logger.debug(data)
            else:
                levels_temp[level - 1][name] = dict()
                levels_temp[level] = levels_temp[level - 1][name]
                logger.debug('set levels_temp[{}] to data[{}]'.format(level, name))
                logger.debug(data)

        else:
            levels_temp[level-1][key] = value

    return data

# read PAN file and return dict of module paramters for PVLIB
def pan_to_module_param(path):

    #group keys of PVSYST 6.7.6
    pan_keys =['PVObject_=pvModule','PVObject_Commercial=pvCommercial','PVObject_IAM=pvIAM','IAMProfile=TCubicProfile','Remarks, Count', 'OperPoints, list of=3 tOperPoint']

    #open file
    with open(path,'r') as file:
        raw = file.read()

    #parse text file to nested dict based on pan_keys
    data = _text_to_dict(raw, pan_keys)
    m = {}

    m['manufacturer'] = (data['PVObject_=pvModule']['PVObject_Commercial=pvCommercial']['Manufacturer'])
    m['module_name'] = (data['PVObject_=pvModule']['PVObject_Commercial=pvCommercial']['Model'])
    m['Technol'] = (data['PVObject_=pvModule']['Technol'])

    m['CellsInS'] = int(data['PVObject_=pvModule']['NCelS'])
    m['CellsInP'] = int(data['PVObject_=pvModule']['NCelP'])
    m['GRef'] = float(data['PVObject_=pvModule']['GRef'])
    m['TRef'] = float(data['PVObject_=pvModule']['TRef'])
    m['Pmpp'] = float(data['PVObject_=pvModule']['PNom'])
    m['Isc'] = float(data['PVObject_=pvModule']['Isc'])
    m['Voc'] = float(data['PVObject_=pvModule']['Voc'])
    m['Impp'] = float(data['PVObject_=pvModule']['Imp'])
    m['Vmpp'] = float(data['PVObject_=pvModule']['Vmp'])

    m['mIsc_percent'] = (float(data['PVObject_=pvModule']['muISC'])/1000/m['Isc'])*100 #PAN stored in mA/C,convert to %/C
    m['mVoc_percent'] = (float(data['PVObject_=pvModule']['muVocSpec'])/1000/m['Voc'])*100 # PAN stored in mV/C, convert to %/C

    m['mIsc'] = float(data['PVObject_=pvModule']['muISC'])/1000  # convert to A/C
    m['mVoc'] = float(data['PVObject_=pvModule']['muVocSpec'])/1000  # convert to V/C

    m['mPmpp'] = float(data['PVObject_=pvModule']['muPmpReq'])
    m['Rshunt'] = float(data['PVObject_=pvModule']['RShunt'])
    m['Rsh 0'] = float(data['PVObject_=pvModule']['Rp_0'])
    m['Rshexp'] = float(data['PVObject_=pvModule']['Rp_Exp'])
    m['Rserie'] = float(data['PVObject_=pvModule']['RSerie'])
    m['Gamma'] = float(data['PVObject_=pvModule']['Gamma'])
    m['muGamma'] = float(data['PVObject_=pvModule']['muGamma'])

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
