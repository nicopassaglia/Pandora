from pandora.shell import netinfo, airmon

def test_ifconfig():
    out = """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.113  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe65:58cd  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:65:58:cd  txqueuelen 1000  (Ethernet)
        RX packets 99349  bytes 6359309 (6.0 MiB)
        RX errors 0  dropped 1  overruns 0  frame 0
        TX packets 115328  bytes 71969213 (68.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

    wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 192.168.1.115  netmask 255.255.255.0  broadcast 192.168.1.255
            inet6 fe80::b060:f8c4:f081:cf17  prefixlen 64  scopeid 0x20<link>
            ether 64:70:02:19:ee:cf  txqueuelen 1000  (Ethernet)
            RX packets 156102  bytes 76017890 (72.4 MiB)
            RX errors 0  dropped 0  overruns 0  frame 0
            TX packets 84793  bytes 5303512 (5.0 MiB)
            TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"""

    ifconfig = netinfo.Ifconfig()
    interfaces = ifconfig._parse(out)
    eth0 = interfaces[0]
    wlan0 = interfaces[1]

    assert eth0['iname'] == 'eth0'
    assert eth0['ipv4'] == '192.168.1.113'
    assert eth0['netmask'] == '255.255.255.0'
    assert wlan0['iname'] == 'wlan0'
    assert wlan0['ipv4'] == '192.168.1.115'
    assert wlan0['netmask'] == '255.255.255.0'

def test_ifconfig2():
    out = """eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.113  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fe65:58cd  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:65:58:cd  txqueuelen 1000  (Ethernet)
        RX packets 109051  bytes 7132766 (6.8 MiB)
        RX errors 0  dropped 1  overruns 0  frame 0
        TX packets 115331  bytes 71969398 (68.6 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan0mon: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        unspec 64-70-02-19-EE-CF-30-30-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 71  bytes 21331 (20.8 KiB)
        RX errors 0  dropped 71  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0"""


    ifconfig = netinfo.Ifconfig()
    interfaces = ifconfig._parse(out)
    eth0 = interfaces[0]
    wlan0 = interfaces[1]
    assert len(interfaces) == 2
    assert eth0['iname'] == 'eth0'
    assert eth0['ipv4'] == '192.168.1.113'
    assert eth0['netmask'] == '255.255.255.0'
    assert wlan0['iname'] == 'wlan0mon'
    assert wlan0.get('ipv4') == None
    assert wlan0.get('netmask') == None

def test_iwconfig():
    out=""""wlan0     IEEE 802.11  ESSID:"CasaColazo"  
          Mode:Managed  Frequency:2.417 GHz  Access Point: 7C:8B:CA:E0:D3:11   
          Bit Rate=72.2 Mb/s   Tx-Power=20 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off
          Link Quality=65/70  Signal level=-45 dBm  
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:1140  Invalid misc:41653   Missed beacon:0"""
    iwconfig = netinfo.Iwconfig()
    mode = iwconfig._parse(out)

    assert mode == 'Managed'

def test_iwconfig2():
    out=""""wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm   
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
          """
    iwconfig = netinfo.Iwconfig()
    mode = iwconfig._parse(out)

    assert mode == 'Monitor'

def test_airmon():
    out="""PHY     Interface       Driver          Chipset

phy0    wlan0           ath9k_htc       Qualcomm Atheros Communications AR9271 802.11n"""
    amon = airmon.Airmon()
    interfaces = amon._parse_get_interfaces(out)
    interface = interfaces[0]
    assert interface[0] == 'phy0'
    assert interface[1] == 'wlan0'

def test_airmon2():
    out="""PHY     Interface       Driver          Chipset

phy0    wlan0           ath9k_htc       Qualcomm Atheros Communications AR9271 802.11n
phy1    wlan1           ath9k_htc       Qualcomm Atheros Communications AR9271 802.11n"""
    amon = airmon.Airmon()
    interfaces = amon._parse_get_interfaces(out)
    assert len(interfaces) == 2
    assert interfaces[0][0] == 'phy0'
    assert interfaces[0][1] == 'wlan0'
    assert interfaces[1][0] == 'phy1'
    assert interfaces[1][1] == 'wlan1'