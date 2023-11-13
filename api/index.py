from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, sys, os

# Pathインスタンスを作成
p = Path()
sys.path.append(os.path.join(str(p.resolve().parent.parent), "Laf"))

file = os.listdir(p.cwd())
#from Laf import respond

# import pinecone
import openai
from llama_index.utils import truncate_text
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # get query from url and strip "q="
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query.strip("q="))
        # get response from respond.py
        # response = respond.get_query(query)
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"{sys.path}".encode("utf-8"))
        self.wfile.write(f"{file}".encode("utf-8"))

        return
