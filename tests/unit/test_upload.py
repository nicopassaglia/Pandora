from unittest import mock
from pandora.core import upload
from requests.exceptions import ConnectionError

class MockResponse():
    def __init__(self, status_code, json):
        self.status_code = status_code
        self.__json = json
    def json(self):
        return self.__json

@mock.patch('pandora.core.upload.requests.post')
def test_get_authenticate1(function_mock):
    function_mock.return_value = MockResponse(200, {'key': 'asd1899e41651sd4f6'})
    assert upload.authenticate('username', 'password') == {'key': 'asd1899e41651sd4f6'}

    function_mock.return_value = MockResponse(404, 'error')
    assert upload.authenticate('username', 'password') == {}

@mock.patch('pandora.core.upload.requests.get')
def test_get_tag1(function_mock):
    function_mock.return_value = MockResponse(200, {'id': 5})
    assert upload.get_tag('5', None) == {'id': 5}

    function_mock.return_value = MockResponse(404, 'error')
    assert upload.get_tag('5', None) is None

@mock.patch('pandora.core.upload.authenticate', return_value={'key': ''})
@mock.patch('pandora.core.upload.get_tag', return_value={'id': '5', 'name': 'example'})
@mock.patch('pandora.core.upload.send_logs_and_delete', return_value=None)
def test_upload1(*args, **kwargs):
    assert upload.upload() == "Wrong credentials!"

@mock.patch('pandora.core.upload.authenticate', return_value={})
@mock.patch('pandora.core.upload.get_tag', return_value={'id': '5', 'name': 'example'})
@mock.patch('pandora.core.upload.send_logs_and_delete', return_value=None)
def test_upload2(*args, **kwargs):
    assert upload.upload() == "Wrong credentials!"

@mock.patch('pandora.core.upload.authenticate', return_value = {'key': 'asdas5d4654'})
@mock.patch('pandora.core.upload.get_tag', return_value = {'id': '5', 'name': 'example'})
@mock.patch('pandora.core.upload.send_logs_and_delete', return_value = None)
def test_upload3(*args, **kwargs):
    assert upload.upload() == "Upload Success"

@mock.patch('pandora.core.upload.authenticate', return_value=ConnectionError)
def test_upload4(authMock):
    authMock.side_effect = ConnectionError()
    assert upload.upload() == "Connection to API failed"
