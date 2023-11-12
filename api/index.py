from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json



class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        #get query from url and strip "q="
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query.strip("q="))

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"あかさたな {query}".encode("utf-8"))
        return
