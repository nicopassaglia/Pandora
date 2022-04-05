import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

TEMP_PATH = os.path.join(ROOT_DIR, 'temp')  # requires `import os`
if not os.path.exists(TEMP_PATH):
    os.mkdir(TEMP_PATH)

LOGS_PATH = os.path.join(ROOT_DIR, 'logs')
if not os.path.exists(LOGS_PATH):
    os.mkdir(LOGS_PATH)

NMAP_PATH = os.path.join(LOGS_PATH, 'nmap')
if not os.path.exists(NMAP_PATH):
    os.mkdir(NMAP_PATH)

AIRODUMP_PATH = os.path.join(LOGS_PATH, 'airodump')
if not os.path.exists(AIRODUMP_PATH):
    os.mkdir(AIRODUMP_PATH)

HTTPREQS_PATH = os.path.join(LOGS_PATH, 'httpreqs')
if not os.path.exists(HTTPREQS_PATH):
    os.mkdir(HTTPREQS_PATH)

DICTS_PATH = os.path.join(ROOT_DIR, 'dicts')
if not os.path.exists(DICTS_PATH):
    os.mkdir(DICTS_PATH)


CONF_PATH = os.path.join(ROOT_DIR, 'conf')  # requires `import os`
if not os.path.exists(CONF_PATH):
    os.mkdir(CONF_PATH)

APACHE_CONFIG_PATH = os.path.join(ROOT_DIR, 'apache_conf')
if not os.path.exists(APACHE_CONFIG_PATH):
    os.mkdir(APACHE_CONFIG_PATH)

PASSWORDS_PATH = os.path.join(ROOT_DIR, 'passwords')
if not os.path.exists(PASSWORDS_PATH):
    os.mkdir(PASSWORDS_PATH)
