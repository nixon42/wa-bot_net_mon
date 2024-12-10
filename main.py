from utils.http_server import start_http_server
from utils.config import CONFIG, NETWORK
from utils.util import print_log
from utils.model import LocalTable, RequestData
from utils.db import Database
from utils.handle_request import process_request

db = Database(":memory:", "local_table")
db.connect()

# Initialize network status dictionary
for network_name in NETWORK:
    # Set initial status for each client in the network
    for client in NETWORK[network_name]:
        ip = NETWORK[network_name][client]
        table = LocalTable(network_name, client, ip, 'up')
        db.insert(table)


def request_handler(cls, requestData: RequestData):
    return process_request(db, requestData)


print_log(f'loaded config {db.fetch_all()}')

start_http_server(request_handler=request_handler, port=CONFIG['http_port'])
