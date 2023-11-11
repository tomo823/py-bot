from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse query string
        parsed_path = urlparse(self.path)
        query = json.loads(parsed_path.query)

        print("Query: " + query)
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write("hello world".encode("utf-8"))
        return 
        # self.send_response(200)
        # self.send_header('Content-type','text/plain')
        # self.end_headers()
        # self.wfile.write('Hello, world!'.encode('utf-8'))
        # return
