'''
this is a ipython notebook style file used to debug code
this is intented to be run with atom hydrogen

'''


%load_ext autoreload
%autoreload 2
import os, sys;

import numpy as np
import pandas as pd


import pprint
pp = pprint.PrettyPrinter(indent=2)


import logging
logger = logging.getLogger('pvsyst')

#%matplotlib inline
#%config InlineBackend.figure_format = 'svg'
import matplotlib.pyplot as plt

from plotly import offline as py
import plotly.tools as tls
import plotly.graph_objs as go
py.init_notebook_mode()


# import pvsyst module based on ipython running in /docs/
cwd = os.getcwd()
print('current workign directory: {}'.format(cwd))
sys.path.append(os.path.dirname(cwd))  # append to path to be able to import module
sys.path.append(os.path.dirname(os.path.dirname(cwd)))  # append to path to be able to import module
import pvsyst
print('pvsyst module path: {}'.format(pvsyst.__file__))

def test_io():
    print()


    pan_file = 'CS3W-440MB-AG_MIX_CSI_PRE_V6_84_1500V_2019 UTF-8-BOM.PAN'
    pan_file = 'CS3W-405PB-AG_MIX_CSIHE_EXT_V6_79_1500V_2019Q2.PAN'

    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/PAN', pan_file)

    logger.setLevel(5)  # 5 for Verbose 10 for Debug

    m = pvsyst.pan_to_module_param(path)
    # df = pd.DataFrame(columns=m.keys(),data = [m.values()])
    m.keys()
    '''
    dict_keys(['manufacturer',
    'module_name',
     'Technol',
     'CellsInS',
      'CellsInP',
       'GRef', 'TRef', 'Pmpp', 'Isc', 'Voc', 'Impp',

        'Vmpp', 'mIsc_percent', 'mVoc_percent', 'mIsc',
        'mVocSpec', 'mPmpp', 'Rshunt', 'Rsh 0', 'Rshexp',
        'Rserie', 'Gamma', 'muGamma', 'IAM', 'gamma_ref',
        'mu_gamma', 'I_L_ref', 'I_o_ref', 'EgRef', 'R_sh_ref',
        'R_sh_0', 'R_s', 'R_sh_exp', 'cells_in_series', 'alpha_sc'])
    '''
    pp.pprint(m)

    data = {"x": m['IAM'][0],"y": m['IAM'][1]}
    py.iplot([data])

    plt.plot(m['IAM'][0],m['IAM'][1])




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

def _test_all():
    df = pd.DataFrame()
    for root, dirs, files in os.walk("data"):
        for file in files:
            if file.lower().endswith(".pan"):

                 pan = os.path.join(root, file)
                 raw = pvsyst.pan_to_module_param(pan)
                 raw['pan_file'] = pan
                 df = df.append(raw,ignore_index=True)
    len(df)
    df['Pmpp'].plot()
    df['Voc'].plot()

    # https://plot.ly/python/parallel-coordinates-plot/




    data = [
        go.Parcoords(
            line = dict(color = df['Pmpp'],
                       colorscale = 'Jet',
                       showscale = True,
                       reversescale = False,
                       cmin = 0,
                       cmax = 400),
            dimensions = list([
                dict(label = 'Pmpp', values = df['Pmpp']),
                dict(label = 'Voc', values = df['Voc']),
                dict(label = 'Isc', values = df['Isc']),
                dict(label = 'Rserie', values = df['Rserie']),
                dict(label = 'Rshunt', values = df['Rshunt'])

            ])
        )
    ]

    py.iplot(data)


def _test_OND():
    ond_file = 'refSMA_Central_2750.OND'
    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/', ond_file)


    logger.setLevel(10)  # 5 for Verbose 10 for Debug

    m = pvsyst.ond_to_inverter_param(path)
    # df = pd.DataFrame(columns=m.keys(),data = [m.values()])

pp.pprint(m)
