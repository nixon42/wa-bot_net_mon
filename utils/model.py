class LocalTable():
    def __init__(self, network_name=None, client_name=None, ip_address=None, status=None, last_down_time=None, last_up_time=None):
        self.network_name = network_name
        self.client_name = client_name
        self.ip_address = ip_address
        self.status = status
        self.last_down_time = last_down_time
        self.last_up_time = last_up_time

    def __str__(self):
        return f"(Network: {self.network_name}, Client: {self.client_name}, IP: {self.ip_address}, Status: {self.status})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            'network_name': self.network_name,
            'client_name': self.client_name,
            'ip_address': self.ip_address,
            'status': self.status,
            'last_down_time': self.last_down_time,
            'last_up_time': self.last_up_time
        }

    def to_tuple(self):
        return (self.network_name, self.client_name, self.ip_address, self.status, self.last_down_time, self.last_up_time)


class RequestData:
    def __init__(self, time_and_date, device_name, device_first_address, device_status):
        self.time_and_date = time_and_date
        self.device_name = device_name
        self.device_first_address = device_first_address
        self.device_status = device_status

    def __str__(self):
        return f"(Time: {self.time_and_date}, Name: {self.device_name}, IP: {self.device_first_address}, Status: {self.device_status})"

    def __repr__(self):
        return self.__str__()
