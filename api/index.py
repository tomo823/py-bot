from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        # json might be cause of error
        query = parsed_path.query
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello, world!".encode("utf-8"))
        self.wfile.write(f"path: {query}".encode("utf-8"))
        return
