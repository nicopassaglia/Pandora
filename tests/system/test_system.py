from pandora.core.ifmanager import InterfaceManager
from pandora.__main__ import get_interfaces

def test_ifmanager():
    ifmanager = InterfaceManager()
    ifmanager.update_interfaces()
    phy, ifname = ifmanager.get_amon_interface_by_phy('phy0')
    interface = ifmanager.switch_mode(ifname, 'Managed')
    assert interface.get('mode') == 'Managed'
    interface = ifmanager.switch_mode(interface['iname'], 'Monitor')
    assert interface.get('mode') == 'Monitor'
    interface = ifmanager.switch_mode(interface['iname'], 'Managed')
    assert interface.get('mode') == 'Managed'

def test_get_interfaces():
    interfaces = get_interfaces()
    assert interfaces == ['wlan0'] or interfaces == ['wlan0mon']