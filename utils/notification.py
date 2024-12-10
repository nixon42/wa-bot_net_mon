from whatsapp_api_client_python import API
from .config import GREENAPI_INSTANCE, GREENAPI_API_KEY, CHAT_ID
from .util import print_log

greenAPI = API.GreenAPI(GREENAPI_INSTANCE, GREENAPI_API_KEY)

NOTIFICATION_TEMPLATE = """
*******************************
    !!!!! NOTIFICATION !!!!!     
*******************************

📍 *NETWORK*    : {network_name}
🎯 *CLIENTS*    : {clients}
🔧 *STATUS*     : {status}
⏰ *TIME*       : {time}
💤 *DOWNTIME*   : {downtime}

------------------------------
"""


def send_notification(msg):
    print_log('send notification')
    greenAPI.sending.sendMessage(CHAT_ID, msg)
