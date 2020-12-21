'''
@author: frederic rivollier
'''

import re, sys, os
import json, struct
import numpy as np
import codecs

from .core import text_to_dict

import logging
logging.addLevelName(5,"VERBOSE")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pysyst')

from pprint import pprint, pformat


# read PAN file and return generic dict
def pan_to_dict(path):

    # group keys of PVSYST 6.7.6
    # key is the start value to identify
    # vaLue is the dict key to be used
    pan_sections ={'PVObject_': 'pvModule',
                'PVObject_Commercial': 'pvCommercial',
                'PVObject_IAM': 'pvIAM',
                'IAMProfile': 'TCubicProfile',
                'Remarks, Count': 'Remarks',
                'OperPoints, list of': 'tOperPoint'}

    #open file
    with open(path, mode='r', encoding='utf-8-sig') as file: # utf-8-sig to fix u'\ufeff' BOM issue on certain OS
        raw = file.read()
        if raw[:3] == "ï»¿": # this is utf-8-BOM
            raw = raw[3:] #remove BOM

    #parse text file to nested dict based on pan_keys
    data = text_to_dict(raw, pan_sections)
    logger.debug(pformat(data))

    '''
    List of PVSYST paramters and units:
    http://files.pvsyst.com/help/pvmodule_parametersummary.htm
    '''
    m = {}

    m['Manufacturer'] = (data['pvModule']['pvCommercial']['Manufacturer'])
    m['Model'] = (data['pvModule']['pvCommercial']['Model'])
    m['Technol'] = (data['pvModule']['Technol'])


    try:
        m['DataSource'] = data['pvModule']['pvCommercial']['DataSource']
        m['YearBeg'] = data['pvModule']['pvCommercial']['YearBeg']
        m['Comment'] = data['pvModule']['pvCommercial']['Comment']
        m['Width'] = float(data['pvModule']['pvCommercial']['Width'])
        m['Height'] = float(data['pvModule']['pvCommercial']['Height'])
        m['Depth'] = float(data['pvModule']['pvCommercial']['Depth'])
        m['Weight'] = float(data['pvModule']['pvCommercial']['Weight'])
    except KeyError:
        pass

    try:
        m['RelEffic800'] = float(data['pvModule']['RelEffic800'])
        m['RelEffic400'] = float(data['pvModule']['RelEffic400'])
        m['RelEffic200'] = float(data['pvModule']['RelEffic200'])
    except KeyError:
        pass

    m['NCelS'] = int(data['pvModule']['NCelS'])
    m['NCelP'] = int(data['pvModule']['NCelP'])
    m['NDiode'] = int(data['pvModule']['NDiode'])

    m['GRef'] = float(data['pvModule']['GRef'])
    m['TRef'] = float(data['pvModule']['TRef'])
    m['PNom'] = float(data['pvModule']['PNom'])
    m['PNomTolLow'] = str(data['pvModule']['PNomTolLow'])
    m['PNomTolUp'] = str(data['pvModule']['PNomTolUp'])

    m['Isc'] = float(data['pvModule']['Isc'])
    m['Voc'] = float(data['pvModule']['Voc'])
    m['Imp'] = float(data['pvModule']['Imp'])
    m['Vmp'] = float(data['pvModule']['Vmp'])

    m['muISC'] = float(data['pvModule']['muISC'])
    m['muVocSpec'] = float(data['pvModule']['muVocSpec'])

    m['muISC'] = float(data['pvModule']['muISC'])
    m['muVocSpec'] = float(data['pvModule']['muVocSpec'])

    m['mIsc_percent'] = (float(data['pvModule']['muISC'])/1000/m['Isc'])*100 #PAN stored in mA/C,convert to %/C
    m['mVoc_percent'] = (float(data['pvModule']['muVocSpec'])/1000/m['Voc'])*100 # PAN stored in mV/C, convert to %/C


    m['muPmpReq'] = float(data['pvModule']['muPmpReq'])

    # RShunt is the RShunt value from PVSYST PAN Files
    # This can be a poor estimate of shunt resistance at G if Rexp is not 5.5
    m['RShunt'] = float(data['pvModule']['RShunt'])
    m['Rp_0'] = float(data['pvModule']['Rp_0'])
    m['Rp_Exp'] = float(data['pvModule']['Rp_Exp'])

    # Recompute RShunt at 1000 W.m2
    # discussion on pvlib https://github.com/pvlib/pvlib-python/issues/1094
    m['RShunt_stc'] = m['RShunt'] + (m['Rp_0'] - m['RShunt']) * np.exp(-m['Rp_Exp']* (1000/m['GRef']))
    m['RSerie'] = float(data['pvModule']['RSerie'])
    m['Gamma'] = float(data['pvModule']['Gamma'])
    m['muGamma'] = float(data['pvModule']['muGamma'])

    '''
      PVObject_Commercial=pvCommercial
        Comment=www.aeg-industrialsolar.de   (Germany) 
        Flags=$0041
        Manufacturer=AEG
        Model=AS-M602G-285
        DataSource=Manufacturer 2017
        YearBeg=2017
        Width=0.998
        Height=1.664
        Depth=0.040
        Weight=25.800
        NPieces=100
        PriceDate=23/12/18 01:22
        Remarks, Count=7
          Str_1=Frame: Black
          Str_2=Structure: 2.5 mm tempered glass x 2 (front glass and back
          Str_3=glass)
          Str_4=Connections: EVA, 2.5 mm tempered glass
          Str_5=Double-glass solar module, PERC, IP67 junction box split-type,
          Str_6=MC-4 compatible cables
          Str_7
        End of Remarks
      End of PVObject pvCommercial

    '''
    try:
        if data['pvModule']['pvCommercial']['Remarks']:
            points = len(data['pvModule']['pvCommercial']['Remarks'])
            comment = []
            for n in range(points):
                v = data['pvModule']['pvCommercial']['Remarks']['Str_{}'.format(n+1)]
                m['REM_Str_{}'.format(n+1)] = v # save the whole tuple for update script

    except Exception as e:
        logger.debug('No remarks found')
        logger.log(5, e)

    # IAM profile to ndarray

    # Options:
    # FrontSurface=fsNormalGlass
    # FrontSurface=fsARCoating
    # if not defined FrontSurface key will not exist
    # FrontSurface=fsPlastic
    # FrontSurface=fsTextured


    '''
    # if Ashre  PVObject_IAM=pvIAM / IAMMode=Ashrae
      PVObject_IAM=pvIAM
        Flags=$00
        IAMMode=Ashrae
        B0_IAM=0.075
      End of PVObject pvIAM

     # if user define FrontSurface key will not exist but  PVObject_IAM=pvIAM
     PVObject_IAM=pvIAM
        Flags=$00
        IAMMode=UserProfile
        IAMProfile=TCubicProfile
          NPtsMax=9
          NPtsEff=9
          LastCompile=$B18D
          Mode=3
          Point_1=10.0,0.99900
          Point_2=20.0,0.99900
          Point_3=30.0,0.99500
          Point_4=40.0,0.99200
          Point_5=50.0,0.98600
          Point_6=60.0,0.97000
          Point_7=70.0,0.91700
          Point_8=80.0,0.76300
          Point_9=90.0,0.00000
        End of TCubicProfile
      End of PVObject pvIAM
  '''
    try:
        if data['pvModule']['pvIAM']['IAMMode'] == 'UserProfile':
            points = int(data['pvModule']['pvIAM']['TCubicProfile']['NPtsEff'])
            x = []
            y = []
            for n in range(points):
                v = data['pvModule']['pvIAM']['TCubicProfile']['Point_{}'.format(n+1)]
                m['IAM_Point_{}'.format(n+1)] = v # save the whole tuple for update script
                # save the individual angle and eff value
                v = v.split(',')
                x.append(float(v[0]))
                # m['IAM_Point_{}_AOI'.format(n+1)] = float(v[0])

                y.append(float(v[1]))
                # m['IAM_Point_{}_EFF'.format(n+1)] = float(v[1])

            m['IAM'] = np.array([x,y])

    except Exception as e:
        logger.debug('IAM profile not found')
        logger.log(5, e)

    '''
    low irradiance
    OperPoints, list of=6 tOperPoint
        Point_1=False,800,25.0,0.00,0.00,0.000,0.000,0.00
        Point_2=False,600,25.0,0.00,0.00,0.000,0.000,0.00
        Point_3=False,400,25.0,0.00,0.00,0.000,0.000,0.00
        Point_4=False,200,25.0,0.00,0.00,0.000,0.000,0.00
        Point_5=False,200,25.0,0.00,0.00,0.000,0.000,0.00
        Point_6=False,200,25.0,0.00,0.00,0.000,0.000,0.00
      End of List OperPoints
    '''

    try:
        if data['pvModule']['tOperPoint']:
            points = len(data['pvModule']['tOperPoint'].keys())
            s = []

            for n in range(points):
                v = data['pvModule']['tOperPoint']['Point_{}'.format(n+1)]
                m['OperPoint_Point_{}'.format(n+1)] = v # save the whole tuple for update script
                # save the individual angle and eff value

    except Exception as e:
        logger.debug('Operating Point profile not found')
        logger.log(5, e)

    '''
    solve IoRef for Pmp
    Using Voc to solve reverse saturation current IoRef based on
    reference: Mermoud, Lejeune (2010): Performance Assessment of a Simulation Model for PV Modules of Any Available Technology.
    Proc 25th European Photovoltaic Solar Energy Conference –Valencia, Spain, 6-10 September 2010

    #PVSYST one diode equation
    http://files.pvsyst.com/help/index.html?pvcell_reversechar.htm

    I  =  Iph  -   Io  [ exp  (q · (V+I·Rs) / ( Ncs·Gamma·k·Tc) ) - 1 ]    -    (V + I·Rs) / Rsh

    with :
    I        =        Current supplied by the module  [A].
    V        =        Voltage at the terminals of the module  [V].
    Iph   [Isc]     =        Photocurrent [A], proportional to the irradiance G,  with a correction as function of  Tc  (see below).
    ID        =        Diode current, is the product   Io  ·  [exp(     ) -1].
    Io  [I_0_ref]      =        inverse saturation current, depending on the temperature [A]  (see expression below).
    Rs        =        Series resistance [ohm].
    Rsh        =        Shunt resistance [ohm].
    q        =        Charge of the electron  =  1.602·E-19 Coulomb
    k        =        Bolzmann's constant =  1.381 E-23  J/K.
    Gamma=          Diode quality factor, normally between 1 and 2
    Ncs        =        Number of cells in series.
    Tc        =        Effective temperature of the cells [Kelvin]
    '''

    #constants
    k = 1.38064852e-23 #Boltzmann’s constant (J/K)
    kelvin0 = 273.15
    q = 1.60217662e-19 # charge of an electron (coulombs)
    GRef = 1000
    Tc = 25 + kelvin0 #Deg Kelvin

    # solving IoRef for Pmax
    # PVSYST manual is not clear on method used by PVSYST i.e. Voc or Pmpp
    # Checked empiricaly agains PVSYST and is the method used by CASSYS
    I = m['Imp']  # solve IoRef for Pmax
    V = m['Vmp']  # solve IoRef for Pmax

    Io = -((I+(V + I*m['RSerie'])/\
                m['RShunt'])-m['Isc'])/\
                (np.exp(q*(V+I*m['RSerie'])/\
                (m['NCelS']*m['Gamma']*k*Tc))-1)

    m['I_o_ref'] = Io
    # TODO

    '''
    # adjust based of m['Technol']
    # from https://en.wikipedia.org/wiki/Multi-junction_solar_cell
    c-Si	1.12
    InGaP	1.86
    GaAs	1.4
    Ge	0.65
    InGaAs	1.2

    # from PVSYST docs
    where	EGap = Gap's energy of the material (:
        1.12  eV  for cristalline Si,
        1.03 eV  for CIS,
        1.7 eV for amorphous silicon,
        1.5 eV for CdTe

    Technol options in PVSYST:
    Si-mono
    Si-poly
    S-EFG
    a-Si:H single
    a-Si:H tandem
    a-Si:H tripple
    uCSI-aSi:H
    CdTe
    CIS
    CSG
    HIT
    GaAs
    GaInP2/GaAs/Ge
    Not Specified

    '''
    m['EgRef'] = 1.121  # The energy bandgap at reference temperature in units of eV

    return m


# read PAN file and return dict of module paramters for PVLIB
def pan_to_module_param(path):

    m = pan_to_dict(path)

    # mapping pvlib mpodule paramters names
    m['manufacturer'] = m['Manufacturer']
    m['module_name'] = m['Model']
    m['Pmpp'] = m['PNom']
    m['Impp'] = m['Imp']
    m['Vmpp'] = m['Vmp']

    m['mIsc'] = m['muISC']/1000  # convert to A/C
    m['mVocSpec'] = m['muVocSpec']/1000  # convert to V/C

    m['mPmpp'] = m['muPmpReq']
    m['Rshunt'] = m['RShunt']
    m['Rsh 0'] = m['Rp_0']
    m['Rshexp'] = m['Rp_Exp']
    m['Rserie'] = m['RSerie']

    m['gamma_ref'] = m['Gamma'] #The diode ideality factor
    m['mu_gamma'] = m['muGamma'] #The temperature coefficient for the diode ideality factor, 1/K
    m['I_L_ref'] = m['Isc'] #The light-generated current (or photocurrent) at reference conditions, in amperes.
    m['R_sh_ref'] = m['RShunt_stc'] #The shunt resistance at reference conditions, in ohms.
    m['R_sh_0'] = m['Rsh 0'] #The shunt resistance at zero irradiance conditions, in ohms.
    m['R_s'] = m['Rserie'] #The series resistance at reference conditions, in ohms.
    m['R_sh_exp'] = m['Rshexp'] #The exponent in the equation for shunt resistance, unitless. Defaults to 5.5.
    m['cells_in_series'] = m['NCelS'] #The number of cells connected in series.
    m['alpha_sc'] = m['mIsc']  #The short-circuit current temperature coefficient of the module in units of A/C.

    return m
