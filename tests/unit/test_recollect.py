from unittest import mock
from pandora.core import recollect

class ErrorTestSpecific(Exception):
    pass

@mock.patch('pandora.core.recollect.NMAP_TARGETS', ['AA:AA:AA:AA:AA:AA', 'BB:BB:BB:BB:BB:BB'])
@mock.patch('pandora.core.recollect.discover_hosts_key_mac', return_value={'AA:AA:AA:AA:AA:AA': '192.168.1.10',
                                                                           'BB:BB:BB:BB:BB:BB': '192.168.1.20',
                                                                           'CC:CC:CC:CC:CC:CC': '192.168.1.30'})
@mock.patch('pandora.core.recollect.nmap.Nmap.save_os', return_value=None)
def test_nmap_job(*args, **kwargs):
    function = recollect.nmap_job
    function('192.168.1.5', '255.255.255.0', 'wlan0')
    assert function.targets == []
    del function.targets

@mock.patch('pandora.core.recollect.NMAP_TARGETS', ['AA:AA:AA:AA:AA:AA', 'BB:BB:BB:BB:BB:BB'])
@mock.patch('pandora.core.recollect.discover_hosts_key_mac', return_value={'AA:AA:AA:AA:AA:AA': '192.168.1.10',
                                                                           'CC:CC:CC:CC:CC:CC': '192.168.1.30'})
@mock.patch('pandora.core.recollect.nmap.Nmap.save_os', return_value=None)
def test_nmap_job2(*args, **kwargs):
    function = recollect.nmap_job
    function('192.168.1.5', '255.255.255.0', 'wlan0')
    assert function.targets == ['BB:BB:BB:BB:BB:BB']
    del function.targets

@mock.patch('pandora.core.recollect.NMAP_TARGETS', [])
@mock.patch('pandora.core.recollect.discover_hosts_key_mac', return_value={'AA:AA:AA:AA:AA:AA': '192.168.1.10',
                                                                           'CC:CC:CC:CC:CC:CC': '192.168.1.30'})
@mock.patch('pandora.core.recollect.nmap.Nmap.save_os', return_value=None)
def test_nmap_job3(*args, **kwargs):
    function = recollect.nmap_job
    function('192.168.1.5', '255.255.255.0', 'wlan0')
    assert function.targets == []
    del function.targets

@mock.patch('pandora.core.recollect.NMAP_TARGETS', ['AA:AA:AA:AA:AA:AA', 'BB:BB:BB:BB:BB:BB'])
@mock.patch('pandora.core.recollect.discover_hosts_key_mac', return_value={})
@mock.patch('pandora.core.recollect.nmap.Nmap.save_os', return_value=None)
def test_nmap_job4(*args, **kwargs):
    function = recollect.nmap_job
    function('192.168.1.5', '255.255.255.0', 'wlan0')
    assert function.targets == ['AA:AA:AA:AA:AA:AA', 'BB:BB:BB:BB:BB:BB']
    del function.targets


@mock.patch('pandora.core.recollect.tshark.Tshark.restart_tshark')
def test_mitm_job(mockTshark, *args, **kwargs):
    mockTshark.side_effect = ErrorTestSpecific()
    #mockTshark.return_value = None
    function = recollect.mitm_job
    function.targetip = 'try'
    try:
        function('192.168.1.5', '255.255.255.0', 'wlan0')
        del function.targetip
        assert False
    except ErrorTestSpecific:
        del function.targetip

@mock.patch('pandora.core.recollect.MITM_TARGET', 'BB:BB:BB:BB:BB:BB')
@mock.patch('pandora.core.recollect.utils.get_default_gateway_linux', return_value='192.168.1.1')
@mock.patch('pandora.core.recollect.discover_hosts_key_mac', return_value={'AA:AA:AA:AA:AA:AA': '192.168.1.10',
                                                                           'BB:BB:BB:BB:BB:BB': '192.168.1.20',
                                                                           'CC:CC:CC:CC:CC:CC': '192.168.1.30'})
def test_mitm_job2(*args, **kwargs):
    function = recollect.mitm_job
    function('192.168.1.5', '255.255.255.0', 'wlan0')
    assert function.targetip == '192.168.1.20'
    del function.targetip

@mock.patch('pandora.core.recollect.MITM_TARGET', 'BB:BB:BB:BB:BB:BB')
@mock.patch('pandora.core.recollect.utils.get_default_gateway_linux', return_value='192.168.1.1')
@mock.patch('pandora.core.recollect.discover_hosts_key_mac', return_value={'AA:AA:AA:AA:AA:AA': '192.168.1.10',
                                                                           'CC:CC:CC:CC:CC:CC': '192.168.1.30'})
def test_mitm_job3(*args, **kwargs):
    function = recollect.mitm_job
    function('192.168.1.5', '255.255.255.0', 'wlan0')
    try:
        function.targetip
        del function.targetip
        assert False
    except AttributeError:
        assert True
