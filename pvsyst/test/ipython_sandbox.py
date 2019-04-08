%load_ext autoreload
%autoreload 2
import os, sys;

import pprint
pp = pprint.PrettyPrinter(indent=2)


import logging
logger = logging.getLogger('pvsyst_io')


# import pvsyst module based on ipython running in /docs/
cwd = os.getcwd()
print('current workign directory: {}'.format(cwd))
sys.path.append(os.path.dirname(cwd))  # append to path to be able to import module
sys.path.append(os.path.dirname(os.path.dirname(cwd)))  # append to path to be able to import module
import pvsyst
print('pvsyst module path: {}'.format(pvsyst.__file__))


def test_io():
    print()



    pan_file = 'check_Canadian_CS3U_350P.PAN'
    pan_file = 'CS3U-365P_MIX_CSIHE_EXT_V6_70_1500V_2018Q2.PAN'

    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/', pan_file)



    logger.setLevel(5)  # 5 for Verbose 10 for Debug

    m = pvsyst.pan_to_module_param(path)
    # df = pd.DataFrame(columns=m.keys(),data = [m.values()])

    pp.pprint(m)

    d = '60.0,0.97000'
    v = d.split(',')
    import numpy as np
    float(v[0])
    x = []
    y = []
    for n in range(9):
        v = d
        v = v.split(',')
        x.append(float(v[0]))
        y.append(float(v[1]))
    x
    m['IAM'] = np.array([x,y])
    m['IAM']
    m['IAM'][1]


def _test_OND():
    ond_file = 'refSMA_Central_2750.OND'
    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/', ond_file)


    logger.setLevel(10)  # 5 for Verbose 10 for Debug

    m = pvsyst.ond_to_inverter_param(path)
    # df = pd.DataFrame(columns=m.keys(),data = [m.values()])

pp.pprint(m)
