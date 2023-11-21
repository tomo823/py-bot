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
from fastapi import FastAPI

time_finish = time.time()

app = FastAPI()

@app.get("/api")
async def hello():
    return {"message": "hello"}

print(time_finish - time_start)

