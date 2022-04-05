from pandora.shell import wash, netinfo, nmap, airmon

def test_wash_parse():
    out = """BSSID               Ch  dBm  WPS  Lck  Vendor    ESSID
--------------------------------------------------------------------------------
EC:08:6B:8D:81:32    1  -82  1.0 No      RealtekS  TP-LINK_8D8132
F8:1A:67:A3:0A:BC    1  -96  1.0  Yes  AtherosC  Flia Oddone 2,4GHz
F8:1A:67:A3:0A:BC    1  -96  1.0  Yes  AtherosC  Flia Oddone
"""

    wps_list = wash.parse_wps_output(out)
    assert wps_list[0]['BSSID'] == 'EC:08:6B:8D:81:32'
    assert wps_list[1]['BSSID'] == 'F8:1A:67:A3:0A:BC'
    assert wps_list[2]['BSSID'] == 'F8:1A:67:A3:0A:BC'
    assert wps_list[0]['ESSID'] == 'TP-LINK_8D8132'
    assert wps_list[1]['ESSID'] == 'Flia Oddone 2,4GHz'
    assert wps_list[2]['ESSID'] == 'Flia Oddone'
    assert wps_list[0]['Lck'] == 'No'
    assert wps_list[1]['Lck'] == 'Yes'
    assert wps_list[2]['Lck'] == 'Yes'
    assert wps_list[0]['WPS'] == '1.0'
    assert wps_list[1]['WPS'] == '1.0'
    assert wps_list[2]['WPS'] == '1.0'

def test_nmap():
    out="""Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-31 21:51 EDT
Nmap scan report for 192.168.1.1
Host is up (0.78s latency).
MAC Address: 7C:8B:CA:A0:D3:CC (Tp-link Technologies)
Nmap scan report for 192.168.1.109
Host is up (0.039s latency).
MAC Address: 00:D8:61:88:99:BB (Micro-star Intl)
Nmap scan report for 192.168.1.114
Host is up (0.034s latency).
MAC Address: 8C:A9:82:E9:C4:AA (Intel Corporate)
Nmap done: 256 IP addresses (3 hosts up) scanned in 53.73 seconds"""
    scanner = nmap.Nmap()
    mac_ip_dict = scanner._parse_key_mac(out)
    tuples = []
    for key_val in mac_ip_dict.items():
        tuples.append(key_val)
    assert tuples[0] == ('7C:8B:CA:A0:D3:CC', '192.168.1.1')
    assert tuples[1] == ('00:D8:61:88:99:BB', '192.168.1.109')
    assert tuples[2] == ('8C:A9:82:E9:C4:AA', '192.168.1.114')

def test_nmap2():
    out="""Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-31 21:51 EDT
Nmap scan report for 192.168.1.1
Host is up (0.78s latency).
MAC Address: 7C:8B:CA:A0:D3:CC (Tp-link Technologies)
Nmap scan report for 192.168.1.109
Host is up (0.039s latency).
Nmap scan report for 192.168.1.114
Host is up (0.034s latency).
MAC Address: 8C:A9:82:E9:C4:AA (Intel Corporate)
Nmap done: 256 IP addresses (3 hosts up) scanned in 53.73 seconds"""
    scanner = nmap.Nmap()
    mac_ip_dict = scanner._parse_key_mac(out)
    tuples = []
    for key_val in mac_ip_dict.items():
        tuples.append(key_val)
    assert len(tuples) == 2
    assert tuples[0] == ('7C:8B:CA:A0:D3:CC', '192.168.1.1')
    assert tuples[1] == ('8C:A9:82:E9:C4:AA', '192.168.1.114')

