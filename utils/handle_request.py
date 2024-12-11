from .model import RequestData, LocalTable
from .util import print_log
from .db import Database
from .notification import send_notification, NOTIFICATION_TEMPLATE
from .config import THRESOLD
import datetime


def format_downtime(last_down_time: float, current_time: float) -> str:
    """Calculate and format the downtime as hours, minutes, and seconds."""
    elapsed_time = current_time - float(last_down_time)
    return str(datetime.timedelta(seconds=int(elapsed_time)))


def notify_network_status(network: list[LocalTable], status: str, downtime: str = '-'):
    """
    Send a notification about the network's status.

    Args:
        network (list[LocalTable]): List of devices in the network.
        status (str): The current status of the network ('up' or 'down').
        downtime (str): The duration of the downtime (optional).
    """
    if not network:
        print_log("No devices found in the network. Notification skipped.")
        return

    # Collect client names from the network
    client_names = [device.client_name for device in network]

    # Prepare and send the notification
    message = NOTIFICATION_TEMPLATE.format(
        network_name=network[0].network_name,
        clients=', '.join(client_names),
        status=status,
        time=datetime.datetime.now(),
        downtime=downtime
    )
    send_notification(message)


def is_network_status(db: Database, network_name: str, expected_status: str) -> bool:
    """
    Check if all devices in a network have the specified status.

    Args:
        db (Database): Database instance.
        network_name (str): Name of the network.
        expected_status (str): The status to check ('up' or 'down').

    Returns:
        bool: True if all devices match the expected status, False otherwise.
    """
    devices = db.fetch_by_network_name(network_name)
    print_log(f'network : {devices}')
    # result = all(device.status == expected_status for device in devices)
    down_count = sum(1 for device in devices if device.status == 'down')
    total_devices = len(devices)
    # Check if the proportion of down devices exceeds or equals the threshold
    result = down_count / total_devices >= THRESOLD

    print_log(f'network check result: {result}')
    return result


def update_device_status(db: Database, request_data: RequestData, existing_device: LocalTable):
    """
    Update the database and send notifications based on the device's status change.

    Args:
        db (Database): Database instance.
        request_data (RequestData): Incoming device status update.
        existing_device (LocalTable): Current database record of the device.
    """
    current_time = datetime.datetime.now().timestamp()

    if request_data.device_status == 'down':
        # Update the last down time
        db.update_field_by_ip(
            request_data.device_first_address, 'last_down_time', current_time)

        # Check if the entire network is down
        if is_network_status(db, existing_device.network_name, 'down'):
            print_log(f'{existing_device.network_name} is down.')
            network_devices = db.fetch_by_network_name(
                existing_device.network_name)
            notify_network_status(network_devices, status='down')

    elif request_data.device_status == 'up':
        # Update the last up time
        db.update_field_by_ip(
            request_data.device_first_address, 'last_up_time', current_time)

        # Check if the entire network is up
        if is_network_status(db, existing_device.network_name, 'up'):
            print_log(f'{existing_device.network_name} is up.')
            network_devices = db.fetch_by_network_name(
                existing_device.network_name)
            downtime = format_downtime(
                existing_device.last_down_time, current_time)
            notify_network_status(
                network_devices, status='up', downtime=downtime)


def process_request(db: Database, request_data: RequestData) -> int:
    """
    Handle incoming device status updates.

    Args:
        db (Database): Database instance.
        request_data (RequestData): Incoming request with device information.

    Returns:
        int: Status code (0 for success, 1 if device not found).
    """
    print_log(f"Processing request: {request_data}")
    existing_device = db.fetch_by_ip(request_data.device_first_address)

    if not existing_device:
        print_log("Device not found in the database.")
        return 1

    # Update client name if it has changed
    if existing_device.client_name != request_data.device_name:
        db.update_field_by_ip(
            request_data.device_first_address, 'client_name', request_data.device_name)

    # Update status if it has changed
    if existing_device.status != request_data.device_status:
        db.update_field_by_ip(
            request_data.device_first_address, 'status', request_data.device_status)
        update_device_status(db, request_data, existing_device)

    return 0
