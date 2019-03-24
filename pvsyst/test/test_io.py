import pvsyst
import os

def test_io():
    print()

    path = os.path.join(os.path.dirname(pvsyst.__file__), r'test/data/CS3U-365P_MIX_CSIHE_EXT_V6_70_1500V_2018Q2.PAN')

    m = pvsyst.pan_file_to_dict(path)
    # df = pd.DataFrame(columns=m.keys(),data = [m.values()])
    print(m)
    
