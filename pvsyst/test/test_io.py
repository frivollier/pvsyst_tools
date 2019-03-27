%load_ext autoreload
%autoreload 2
import os, sys
import pprint
pp = pprint.PrettyPrinter(indent=2)

def test_io():
    print()

    # import pvsyst module based on ipython running in /docs/
    cwd = os.getcwd()
    print('current workign directory: {}'.format(cwd))
    sys.path.append(os.path.dirname(cwd))  # append to path to be able to import module
    sys.path.append(os.path.dirname(os.path.dirname(cwd)))  # append to path to be able to import module
    import pvsyst
    print('pvsyst module path: {}'.format(pvsyst.__file__))

    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/CS3U-365P_MIX_CSIHE_EXT_V6_70_1500V_2018Q2.PAN')

    import logging
    logger = logging.getLogger('pvsyst_io')
    logger.setLevel(10)

    m = pvsyst.pan_to_module_param(path)
    # df = pd.DataFrame(columns=m.keys(),data = [m.values()])

    pp.pprint(m)
