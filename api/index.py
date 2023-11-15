from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

import json, sys, os, re, glob, urllib.parse, time
import pinecone
import openai
from dotenv import load_dotenv
from llama_index.utils import truncate_text
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore


# Setting up environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment="us-west4-gcp-free")


# Sources:
folder_list = [
    "./movies/【高校数学1】数と式",
    "./movies/【中1数学】一次方程式",
    "./movies/【中1数学】空間図形",
    "./movies/【中1数学】正の数・負の数",
    "./movies/【中1数学】比例・反比例",
    "./movies/【中1数学】文字式",
    "./movies/【中1数学】平面図形",
    "./movies/【中1数学】資料の活用",
    "./movies/【中2数学】一次関数",
    "./movies/【中2数学】確率",
    "./movies/【中2数学】三角形と四角形",
    "./movies/【中2数学】式の計算",
    "./movies/【中2数学】平行線・多角形・合同",
    "./movies/【中2数学】連立方程式",
    "./movies/【中3数学】三平方の定理",
    "./movies/【中3数学】式の展開と因数分解",
    "./movies/【中3数学】相似な図形",
    "./movies/【中3数学】二次関数",
    "./movies/【中3数学】二次方程式",
    "./movies/【中3数学】平方根",
    "./movies/【中3数学】円",
    "./movies/【高校数学1】集合と命題",
    "./movies/【高校数学1】データの分析/",
    "./movies/【高校数学1】図形と計量",
]


# connect to idex in pinecone
pinecone_index = pinecone.Index("keyword-search")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="pg_essay_0.6.0")
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# the number of references which user will get
query_engine = index.as_query_engine(
    similarity_top_k=1,
)


def get_query(query):
    # get query from user
    if query == None:
        return "Please enter a query"
    else:
        pass
    response = query_engine.query(query)

    source_text_fmt = truncate_text(response.source_nodes[0].node.get_content().strip(), 350)
    # reference for response
    reference = source_text_fmt.strip("...")

    # Getting the title of the Reference
    Dict = {}
    key = []
    for files in folder_list:
        path_list = glob.glob(files + "/*")
        for path in path_list:
            # print(f"Path: {path}")
            with open(path, "r") as f:
                text = f.read()
                # Comparing the text of the node with the text of the response
                if reference in text:
                    # Obtain a path as a key, text as value
                    Dict[path] = text
                    # Confirmation
                    # print(f"Pathの出力:\n{path}")
                    # Make a list of keys
                    key.append(path)
                    # print(type(re.sub(r'\..*\/', '', dict[path].keys())))

    # getting url of the reference
    with open("URL.json") as f:
        d = json.load(f)
        for i in d.values():
            for j in key:
                # Get only the file name from the key and assign it to i. type == str.
                if i == re.sub(r"\..*\/", "", j).rstrip(".txt"):
                    # urls.append(i)
                    keys = [k for k, v in d.items() if v == i]
    print(keys)
    return str(re.sub(r"\..*\/", "", key[0]).rstrip(".txt"))


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query from url
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query).strip("q=")
        encoded_text = unquote(query)

        # Get answer from query
        answer = get_query(encoded_text)

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        # Display query
        self.wfile.write(f"question: {encoded_text}".encode("utf-8"))
        self.wfile.write(f"Answer: {answer}".encode("utf-8"))
        self.wfile.write(f"\n".encode("utf-8"))
        self.wfile.write(os.getenv("OPENAI_API_KEY").encode("utf-8"))
        self.wfile.write(os.getenv("PINECONE_API_KEY").encode("utf-8"))
        return
