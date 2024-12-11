import json
import os

THRESOLD = 0.8
GREENAPI_INSTANCE = os.environ['GREENAPI_INSTANCE']
GREENAPI_API_KEY = os.environ['GREENAPI_API_KEY']
CHAT_ID = os.environ['CHAT_ID']

conf_dir_files = os.listdir('conf.d')

with open('config.json') as f:
    CONFIG = json.load(f)

THRESOLD = CONFIG['thresold']
NETWORK = {}

for n in conf_dir_files:
    network_name = n.replace('.json', '')
    with open('conf.d/'+n) as f:
        NETWORK[network_name] = json.load(f)
