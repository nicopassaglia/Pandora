from pandora.core import crack
from unittest import mock




@mock.patch('pandora.core.crack.TARGET_SSID', 'Pruebas')
def test_get_target_ap1(*args, **kwargs):
    aps = [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'}, 
    {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'}, 
    {'ESSID': 'Pruebas3', 'BSSID': ' CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}]
    assert crack.get_target_ap(aps) == {'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'}

@mock.patch('pandora.core.crack.TARGET_SSID', 'Pruebas3')
def test_get_target_ap2(*args, **kwargs):
    aps = [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'}, 
    {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'}, 
    {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}]
    assert crack.get_target_ap(aps) == {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}

@mock.patch('pandora.core.crack.TARGET_SSID', 'Pruebas')
@mock.patch('pandora.core.crack._wep', return_value=True)
@mock.patch('pandora.core.crack._wps', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack.airodump.Airodump.get_airodump', return_value=(
    [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'},
     {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'},
     {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}], []))
@mock.patch('pandora.core.crack.wash.Wash.get_wps_info', return_value=[{'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'WPS': '1.0', 'Lck': 'No'}])
def test_crack_tree1(*args, **kwargs):
    assert crack.crack_tree('wlan0') == 3

@mock.patch('pandora.core.crack.TARGET_SSID', 'Pruebas2')
@mock.patch('pandora.core.crack._wep', return_value=True)
@mock.patch('pandora.core.crack._wps', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack.airodump.Airodump.get_airodump', return_value=(
    [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'},
     {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'},
     {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}], []))
@mock.patch('pandora.core.crack.wash.Wash.get_wps_info', return_value=[{'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'WPS': '1.0', 'Lck': 'No'}])
def test_crack_tree2(*args, **kwargs):
    assert crack.crack_tree('wlan0') == 2

@mock.patch('pandora.core.crack.TARGET_SSID', 'Pruebas3')
@mock.patch('pandora.core.crack._wep', return_value=True)
@mock.patch('pandora.core.crack._wps', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack.airodump.Airodump.get_airodump', return_value=(
    [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'},
     {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'},
     {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}], []))
@mock.patch('pandora.core.crack.wash.Wash.get_wps_info', return_value=[{'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'WPS': '1.0', 'Lck': 'No'}])
def test_crack_tree3(*args, **kwargs):
    assert crack.crack_tree('wlan0') == 1

@mock.patch('pandora.core.crack.TARGET_SSID', 'No existe')
@mock.patch('pandora.core.crack._wep', return_value=True)
@mock.patch('pandora.core.crack._wps', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack.airodump.Airodump.get_airodump', return_value=(
    [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'WPA2'},
     {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'},
     {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}], []))
@mock.patch('pandora.core.crack.wash.Wash.get_wps_info', return_value=[{'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'WPS': '1.0', 'Lck': 'No'}])
def test_crack_tree4(*args, **kwargs):
    assert crack.crack_tree('wlan0') == -1


@mock.patch('pandora.core.crack.TARGET_SSID', 'Pruebas')
@mock.patch('pandora.core.crack._wep', return_value=True)
@mock.patch('pandora.core.crack._wps', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack._wpa', return_value=True)
@mock.patch('pandora.core.crack.airodump.Airodump.get_airodump', return_value=(
    [{'ESSID': 'Pruebas', 'BSSID': 'AA:AA:AA:AA:AA:AA', 'Privacy': 'ERROR'},
     {'ESSID': 'Pruebas2', 'BSSID': 'BB:BB:BB:BB:BB:BB', 'Privacy': 'WEP'},
     {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}], []))
@mock.patch('pandora.core.crack.wash.Wash.get_wps_info', return_value=[{'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'WPS': '1.0', 'Lck': 'No'}])
def test_crack_tree5(*args, **kwargs):
    assert crack.crack_tree('wlan0') == -1




reaver_output1="""Reaver v1.6.6-git-1-g4316c26 WiFi Protected Setup Attack Tool                                                                                                                                                                              
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>                                                                                                                                                     
                                                                                                                                                                                                                                           
executing pixiewps -e acae1d7566ae1749b7342ea806c9e6866ea406cdee9adfa4127a328fc9edb03309d08c0284fb6c51b3c921e5ce098cecd30f561eedad2182ddad7383b42525f27620c77a609755ac801b85269d8b0add542d049a0900480c613e86fd255f012ebebac1cd965b50667f05d8009087b792acd5339097c9a7c6234c88ff99cd784522d1edac53483cba7de1ac63778ef3e5c47fa5b7b0df3fccb630bb42336dfe83b56f1ddee5e37ab9beef55c93c32507006d180606f72b04a6a3340a484f97583 -s a51bf92fe6a5cd741c0eeb70e21401c918ad22d2ae13fcf419e0ac7b6d6a313e -z c35ca7579e798874515bc8a738b53770b836bf1d23f7b299930ae12cfd5ed87d -a 85daee14dd6ddeffaef795209488904495fc0d09841aa6936175f6ebae84dda5 -n 4ba8594632c9c0b4beb9938f6067179e -r 3c4352ee904595f484b1b27def3c269cab0f9804e5ab0f1b6cff08727053a2fb912ceac5e649a1d8c4f6cf1a4580bf38eb8f7de21dbb3a60fd1d2c55108280c5e54593a014aa50cfc17be6583c6cf9ee10357ae6424d1742b71457183a3431edbd62bcae7aa5d4aeb724013dfaf63af5028771ecd01b29f3301e38a4f5b67a601eb0059f73d677dcc59ed3217af4e4dd12ef6d257a541bf3b0d1f7b3ecd89a23af5aaebd55bc2851b87fa65dc0a26543fd27d623a4450d56c33c12bd410d5676                                                                                                                                             
                                                                                                                                                                                                                                           
 Pixiewps 1.4                                                                                                                                                                                                                              
                                                                                                                                                                                                                                           
 [?] Mode:     1 (RT/MT/CL)                                                                                                                                                                                                                
 [*] Seed N1:  0xa2e2409e                                                                                                                                                                                                                  
 [*] Seed ES1: 0x678b875f                                                                                                                                                                                                                  
 [*] Seed ES2: 0x53b140bf                                                                                                                                                                                                                  
 [*] PSK1:     7a291d5d450133eb9f266fb859781325                                                                                                                                                                                            
 [*] PSK2:     8175c415ee2e9c913ea9f4fc0236e7f5                                                                                                                                                                                            
 [*] ES1:      9aebd9a2d773a58cdf7e4224fcfe7b46                                                                                                                                                                                            
 [*] ES2:      9e14c3f91f95d32aea2b38130301c2c3                                                                                                                                                                                            
 [+] WPS pin:  70344325                                                                                                                                                                                                                    
                                                                                                                                                                                                                                           
 [*] Time taken: 0 s 97 ms                                                                                                                                                                                                                 
                                                                                                                                                                                                                                           
[+] WPS PIN: '70344325'                                                                                                                                                                                                                    
[+] WPA PSK: 'password'                                                                                                                                                                                                                    
[+] AP SSID: 'Colazo2,4Ghz'  
"""

reaver_output2="""Reaver v1.6.6-git-1-g4316c26 WiFi Protected Setup Attack Tool                                                                                                                                                                              
Copyright (c) 2011, Tactical Network Solutions, Craig Heffner <cheffner@tacnetsol.com>                                                                                                                                                     
                                                                                                                                                                                                                                           
executing pixiewps -e acae1d7566ae1749b7342ea806c9e6866ea406cdee9adfa4127a328fc9edb03309d08c0284fb6c51b3c921e5ce098cecd30f561eedad2182ddad7383b42525f27620c77a609755ac801b85269d8b0add542d049a0900480c613e86fd255f012ebebac1cd965b50667f05d8009087b792acd5339097c9a7c6234c88ff99cd784522d1edac53483cba7de1ac63778ef3e5c47fa5b7b0df3fccb630bb42336dfe83b56f1ddee5e37ab9beef55c93c32507006d180606f72b04a6a3340a484f97583 -s a51bf92fe6a5cd741c0eeb70e21401c918ad22d2ae13fcf419e0ac7b6d6a313e -z c35ca7579e798874515bc8a738b53770b836bf1d23f7b299930ae12cfd5ed87d -a 85daee14dd6ddeffaef795209488904495fc0d09841aa6936175f6ebae84dda5 -n 4ba8594632c9c0b4beb9938f6067179e -r 3c4352ee904595f484b1b27def3c269cab0f9804e5ab0f1b6cff08727053a2fb912ceac5e649a1d8c4f6cf1a4580bf38eb8f7de21dbb3a60fd1d2c55108280c5e54593a014aa50cfc17be6583c6cf9ee10357ae6424d1742b71457183a3431edbd62bcae7aa5d4aeb724013dfaf63af5028771ecd01b29f3301e38a4f5b67a601eb0059f73d677dcc59ed3217af4e4dd12ef6d257a541bf3b0d1f7b3ecd89a23af5aaebd55bc2851b87fa65dc0a26543fd27d623a4450d56c33c12bd410d5676                                                                                                                                             
                                                                                                                                                                                                                                           
 Pixiewps 1.4                                                                                                                                                                                                                              
                                                                                                                                                                                                                                           
 [?] Mode:     1 (RT/MT/CL)                                                                                                                                                                                                                
 [*] Seed N1:  0xa2e2409e                                                                                                                                                                                                                  
 [*] Seed ES1: 0x678b875f                                                                                                                                                                                                                  
 [*] Seed ES2: 0x53b140bf                                                                                                                                                                                                                  
 [*] PSK1:     7a291d5d450133eb9f266fb859781325                                                                                                                                                                                            
 [*] PSK2:     8175c415ee2e9c913ea9f4fc0236e7f5                                                                                                                                                                                            
 [*] ES1:      9aebd9a2d773a58cdf7e4224fcfe7b46                                                                                                                                                                                            
 [*] ES2:      9e14c3f91f95d32aea2b38130301c2c3                                                                                                                                                                                            
 [+] WPS pin:  70344325                                                                                                                                                                                                                    
                                                                                                                                                                                                                                           
 [*] Time taken: 0 s 97 ms                                                                                                                                                                                                                  
"""

@mock.patch('pandora.core.crack.bully.Bully.bully', return_value=reaver_output1)
@mock.patch('pandora.core.crack._write_pw_to_file', return_value=None)
def test_wps1(*args, **kwargs):
    target_ap = {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}
    ifname = 'wlan0'
    assert crack._wps(target_ap, ifname) == True

@mock.patch('pandora.core.crack.bully.Bully.bully', return_value=reaver_output2)
@mock.patch('pandora.core.crack._write_pw_to_file', return_value=None)
def test_wps2(*args, **kwargs):
    target_ap = {'ESSID': 'Pruebas3', 'BSSID': 'CC:CC:CC:CC:CC:CC', 'Privacy': 'WPA'}
    ifname = 'wlan0'
    assert crack._wps(target_ap, ifname) == False

wep1 = """[5;18H[00:00:02] Tested 579553 keys (got 6626 IVs)[0K[7;4HKB    depth   byte(vote)
    0   27/ 29   CF(8704) 18(8448) 48(8448) 50(8448) 78(8448) 
    1   47/ 48   2D(7936) 05(7680) 0D(7680) 17(7680) 22(7680) 
    2   43/  2   E9(7936) 19(7680) 1B(7680) 2A(7680) 4D(7680) 
    3    3/  6   A9(10240) 1D(9984) 4B(9984) A7(9472) BE(9472) 
    4   42/  4   FD(7936) 0F(7680) 17(7680) 19(7680) 23(7680) 
[0J
[0K[21CKEY FOUND! [ 72:65:64:65:73 ] (ASCII: redes )
	Decrypted correctly: 100%"""

wep2 = """[5;18H[00:00:02] Tested 579553 keys (got 6626 IVs)[0K[7;4HKB    depth   byte(vote)
    0   27/ 29   CF(8704) 18(8448) 48(8448) 50(8448) 78(8448) 
    1   47/ 48   2D(7936) 05(7680) 0D(7680) 17(7680) 22(7680) 
    2   43/  2   E9(7936) 19(7680) 1B(7680) 2A(7680) 4D(7680) 
    3    3/  6   A9(10240) 1D(9984) 4B(9984) A7(9472) BE(9472) 
    4   42/  4   FD(7936) 0F(7680) 17(7680) 19(7680) 23(7680) 
	Decrypted correctly: 100%"""


@mock.patch('pandora.core.crack._write_pw_to_file', return_value=None)
def test_wep1(*args, **kwargs):
    assert crack._check_wep_and_write(wep1) == True
    assert crack._check_wep_and_write(wep2) == False
