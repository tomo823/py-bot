from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, quote

# from urllib.parse import parse_qs, urlencode, quote, unquote
# from pathlib import Path
# import json, sys, os, re, glob, urllib.parse, time


# import pinecone
# import openai
# from dotenv import load_dotenv
# from llama_index.utils import truncate_text
# from llama_index import VectorStoreIndex
# from llama_index.vector_stores import PineconeVectorStore


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query).strip("q=")
        encoded_text = quote(query)

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"question: {encoded_text}".encode("utf-8"))
        return
