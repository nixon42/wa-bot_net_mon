import http.server
import socketserver
import urllib.parse
import json
from .model import RequestData


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    callback = None

    @classmethod
    def set_callback(cls, callback_function):
        cls.callback = callback_function

    def do_GET(self):
        try:
            # Parse the URL and query parameters
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)

            # Check if all required parameters exist
            required_params = ['params']
            if not all(param in query_params for param in required_params):
                self.send_error(400, "Missing required parameters")
                return

            params = query_params['params'][0]
            param_list = params.split(';')
            # Create RequestData object
            request_data = RequestData(
                '',
                param_list[0],
                param_list[1],
                param_list[2]
            )

            # Execute callback if set
            r_code = self.callback(request_data)

            if r_code != 0:
                # send error response
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'status': 'failed',
                    'mesage': 'internal server error'
                }
                self.wfile.write(json.dumps(response).encode())
                return

            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'success',
                'message': 'Request received successfully',
                'data': {
                    'time_and_date': request_data.time_and_date,
                    'device_name': request_data.device_name,
                    'device_first_address': request_data.device_first_address,
                    'device_status': request_data.device_status
                }
            }
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_error(500, str(e))


def start_http_server(request_handler, port=8000):
    """Start a simple HTTP Get server"""
    handler = CustomHTTPRequestHandler
    handler.set_callback(request_handler)

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()


if __name__ == "__main__":
    start_http_server()
