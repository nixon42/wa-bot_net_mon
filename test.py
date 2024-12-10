from utils.model import RequestData
from utils.config import CONFIG
import requests
import datetime

data = RequestData(
    datetime.datetime.now().isoformat(),
    'TOl',
    '10.1.2.234',
    'up'
)

res = requests.get(f'http://127.0.0.1:{CONFIG["http_port"]}/?TimeAndDate={data.time_and_date}&DeviceName={
                   data.device_name}&DeviceFirstAddress={data.device_first_address}&DeviceStatus={data.device_status}')

print(res.json())
