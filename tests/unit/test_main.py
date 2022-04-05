from unittest import mock
from argparse import ArgumentTypeError
from datetime import datetime
from pandora.__main__ import get_interfaces, validate_datetime, validate_targetmac


@mock.patch('pandora.__main__.airmon.Airmon.get_interfaces', return_value=[('phy0', 'wlan0'), ('phy1', 'wlan1')])
def test_get_interfaces1(*args, **kwargs):
    assert get_interfaces() == ['wlan0', 'wlan1']

@mock.patch('pandora.__main__.airmon.Airmon.get_interfaces', return_value=[])
def test_get_interfaces2(*args, **kwargs):
    assert get_interfaces() == []

@mock.patch('pandora.__main__.airmon.Airmon.get_interfaces', return_value=[('phy0', 'wlan0')])
def test_get_interfaces3(*args, **kwargs):
    assert get_interfaces() == ['wlan0']

def test_validate_targetmac1():
    assert validate_targetmac("CC:CC:CC:CC:CC:CC") == "CC:CC:CC:CC:CC:CC"
    assert validate_targetmac("Ff:fF:15:aA:cE:45") == "Ff:fF:15:aA:cE:45"

def test_validate_targetmac2():
    try:
        validate_targetmac("AA:AA:AA:AA:AA")
        assert False
    except ArgumentTypeError:
        assert True

def test_validate_targetmac3():
    try:
        validate_targetmac("AA:AA:AA:AA:AA:a")
        assert False
    except ArgumentTypeError:
        assert True

def test_validate_datetime1():
    #"%d/%m/%y-%H:%M"
    assert validate_datetime('10/10/20-10:00') == datetime(2020, 10, 10, 10, 0)
    assert validate_datetime('15/10/20-16:01') == datetime(2020, 10, 15, 16, 1)

def test_validate_datetime2():
    #"%d/%m/%y-%H:%M"
    #Invalid month
    try:
        validate_datetime('15/13/20-16:01')
        assert False
    except ArgumentTypeError:
        assert True

    try:
        validate_datetime('15/13/20-25:66')
        assert False
    except ArgumentTypeError:
        assert True

def test_validate_datetime3():
    #"%d/%m/%y-%H:%M"
    #Invalid format
    try:
        validate_datetime('15/13/20.16:01')
        assert False
    except ArgumentTypeError:
        assert True

def test_validate_datetime4():
    #"%d/%m/%y-%H:%M"
    #Invalid format
    try:
        validate_datetime('15/13/20-16:011')
        assert False
    except ArgumentTypeError:
        assert True

def test_validate_datetime5():
    #"%d/%m/%y-%H:%M"
    #Invalid format
    try:
        validate_datetime('15/13/20-16.01')
        assert False
    except ArgumentTypeError:
        assert True
