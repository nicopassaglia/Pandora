import os
from pandora.shell.airodump import Airodump

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

TEST_PATH = os.path.join(ROOT_DIR, 'files')  # requires `import os`

def test_airodump():
    adump = Airodump(dirpath=TEST_PATH)
    accps, stations = adump.parse_csv()
    assert accps[0]['ESSID'] == 'WiFi-y7aj_2,4'
    assert accps[1]['BSSID'] == 'E4:BE:ED:C3:61:90'
    assert stations[0]['Station MAC'] == '60:30:D4:6A:16:0A'
    assert stations[1]['Station MAC'] == 'B0:E8:92:E3:50:7D'
