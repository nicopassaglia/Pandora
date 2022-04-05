from unittest import mock
from pandora.core import ifmanager


@mock.patch("pandora.core.ifmanager.netinfo.Ifconfig.get_interfaces", return_value=[{'iname': 'wlan0', 'ipv4': '192.168.1.50', 'netmask': '255.255.255.0'}])
@mock.patch("pandora.core.ifmanager.netinfo.Iwconfig.get_mode", return_value='Managed')
def test_ifmanager1(*args, **kwargs):
    imanager = ifmanager.InterfaceManager()
    imanager.update_interfaces()
    assert imanager.get_interfaces() == [{'iname': 'wlan0', 'ipv4': '192.168.1.50', 'netmask': '255.255.255.0', 'mode': 'Managed'}]


def test_ifmanager2(*args, **kwargs):
    imanager = ifmanager.InterfaceManager()
    imanager.interfaces = [{'iname': 'wlan0', 'ipv4': '192.168.1.50', 'netmask': '255.255.255.0', 'mode': 'Managed'}, {'iname': 'wlan1', 'ipv4': '192.168.1.40', 'netmask': '255.255.255.0', 'mode': 'Managed'}]
    assert imanager.get_interface_by_name('wlan1') == {'iname': 'wlan1', 'ipv4': '192.168.1.40', 'netmask': '255.255.255.0', 'mode': 'Managed'}

@mock.patch("pandora.core.ifmanager.airmon.Airmon.get_interfaces", return_value=[('phy0', 'wlan0'), ('phy1', 'wlan1mon')])
def test_ifmanager3(*args, **kwargs):
    imanager = ifmanager.InterfaceManager()
    assert imanager.get_amon_interface_by_name('wlan1mon') == ('phy1', 'wlan1mon')

@mock.patch("pandora.core.ifmanager.airmon.Airmon.get_interfaces", return_value=[('phy0', 'wlan0'), ('phy1', 'wlan1mon'), ('phy2', 'wlan2')])
def test_ifmanager4(*args, **kwargs):
    imanager = ifmanager.InterfaceManager()
    assert imanager.get_amon_interface_by_phy('phy2') == ('phy2', 'wlan2')