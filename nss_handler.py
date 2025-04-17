from enum import Enum
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler


class status(Enum):
    HTTP_200_SUCCESS = 200
    HTTP_201_SUCCESS_CREATED = 201
    HTTP_204_SUCCESS_NO_RESPONSE_BODY = 204
    HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA = 400
    HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND = 404
    HTTP_500_SERVER_ERROR = 500

class HandleRequests(BaseHTTPRequestHandler):

    # Method to send an HTTP response to the client
    def response(self, body, code):
        # Set the HTTP response code
        self.set_response_code(code)
        # Convert response body (as a string) to bytes
        # && write it to the response stream
        self.wfile.write(body.encode())

    # Method to parse a URL path to extract resource information, query params, and pk
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        # Use Python's urlparse to break down the URL
        parsed_url = urlparse(path)
        # Split the URL path by slashes
        path_params = parsed_url.path.split('/')
        # Get resource name - which will be the first segment after initial slash
        resource = path_params[1]

        # Create a dictionary to store URL info
        url_dictionary = {
            "requested_resource": resource,
            "query_params": {},
            "pk": 0
        }

        # Check if there are query params in the URL
        if parsed_url.query:
            # Parse the query string into a dictionary
            query = parse_qs(parsed_url.query)
            # Store query params in the dictionary
            url_dictionary["query_params"] = query

        # Try to extract a pk from the URL path
        try:
            # Attempt to get and convert the 3rd URL segment to an integer
            pk = int(path_params[2])
            # Store it as the url pk in url_dictionary
            url_dictionary["pk"] = pk
        # Continue if error is thrown where no pk exists or pk is not an integer
        except (IndexError, ValueError):
            pass

        # Return the parsed URL info
        return url_dictionary

    # Method to set up the HTTP response headers
    def set_response_code(self, status):
        # Send the HTTP status code
        self.send_response(status)
        # Indicate JSON response content
        self.send_header('Content-type', 'application/json')
        # Enable CORS (allows requests from any origin)
        self.send_header('Access-Control-Allow-Origin', '*')
        # Finishes the headers section
        self.end_headers()

    # Method to handle HTTP OPTIONS requests, used for CORS preflight requests
    def do_OPTIONS(self):
        # Send 200 OK status
        self.send_response(200)
        # Allow requests from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        # Specify allowed HTTP methods
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        # Specify allowed request headers
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        # Finish the headers section
        self.end_headers()

# CORS == Cross-Origin Resource Sharing