from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, sys
from pathlib import Path
#add path to respond.py which is in the parent directory

current_dir = Path(__file__)
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from Laf import respond


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        #get query from url and strip "q="
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query.strip("q="))
        #get response from respond.py
        response = respond.get_query(query)
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"{response}".encode("utf-8"))
        return
