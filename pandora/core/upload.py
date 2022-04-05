import os
import requests
from pandora.config import USERNAME, PASSWORD, API, TAG_FOLDER_LIST, UNACCEPTED_EXTENSIONS

def upload():
    try:
        #Authenticate
        key = authenticate(USERNAME, PASSWORD)
        if key.get('key') and len(key.get('key')) > 0:
            token = 'Token ' + key.get('key')
            auth_header = {'Authorization': token}
            for tag_id, folderpath in TAG_FOLDER_LIST:
            #Check if tag exists
                tag = get_tag(tag_id, auth_header)
                if tag is not None and tag.get('id'):
                    #Upload files associated with that tag
                    send_logs_and_delete(folderpath, tag_id, auth_header)
            msg = "Upload Success"
        else:
            msg = "Wrong credentials!"
    except requests.exceptions.ConnectionError:
        msg = "Connection to API failed"
    print(msg)
    return msg

def get_tag(tag_id, auth_header):
    tag_url = "".join([API, "/tags/", tag_id])
    resp = requests.get(tag_url, headers=auth_header)
    if resp.status_code == 200:
        tag = resp.json()
    else:
        tag = None
    return tag

def authenticate(username, password):
    loginurl = "".join([API, "/auth/login/"])
    payload = {'username': username, 'password': password}
    resp = requests.post(loginurl, data=payload)
    return resp.json() if resp.status_code == 200 else {}

def send_logs_and_delete(folderpath, tag_id, auth_header):
    #Check if file is opened by another process.
    #Send files of a folder
    #Delete file sent
    #Chequear extension del arhivo para no mandar los ivs?
    #Chequear extensiones correctas y mandar, sino borrar? Lista con extensiones correctas.
    filenames = []
    for _, _, files in os.walk(folderpath):
        filenames.extend(files)
        break
    for filename in filenames:
        extension = filename.split(".")[-1]
        filepath = os.path.join(folderpath, filename)
        if extension in UNACCEPTED_EXTENSIONS:
            os.remove(filepath)
        else:
            response = post_file(filepath, tag_id, auth_header)
            if response.status_code == 201:
                os.remove(filepath)


def post_file(filepath, tag_id, auth_header):
    url = "".join([API, "/files/"])
    fh = open(filepath, 'rb')
    files = {'file': fh}
    payload = {'tag': tag_id}
    response = requests.post(url, files=files, data=payload, headers=auth_header)
    fh.close()
    return response
