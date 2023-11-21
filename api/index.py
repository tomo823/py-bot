import time

time_start = time.time()

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

import json, os, re, glob, logging
import pinecone
import openai
from dotenv import load_dotenv
from llama_index.utils import truncate_text
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore
from llama_index.callbacks import CallbackManager, LlamaDebugHandler, CBEventType
from llama_index import ListIndex, ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index import ServiceContext, LLMPredictor, TreeIndex
from llama_index.llms import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("from logger")
print("from print")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query from url
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query).strip("q=")
        encoded_text = unquote(query)
        # Get answer from query
        # url, title = get_query(encoded_text)
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        # Display query
        self.wfile.write(f"question: {encoded_text}".encode("utf-8"))
        self.wfile.write(f"\n".encode("utf-8"))
        # self.wfile.write(f"Url: {url}, Title: {title}".encode("utf-8"))
        return
