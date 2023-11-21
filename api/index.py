import time

time_start = time.time()

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

import json, os, re, glob
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

print("Loading...")


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


# # Setting up environment variables
# env_file_path = "../.env"
# # Write your API keys in .env file
# with open(env_file_path, "r") as f:
#     for line in f:
#         # Ignore comment lines and blank lines
#         if line.strip() and not line.strip().startswith("#"):
#             key, value = line.strip().split("=", 1)
#             os.environ[key] = value


openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment="us-west4-gcp-free")


llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])
llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
service_context = ServiceContext.from_defaults(llm=llm, callback_manager=callback_manager)

# connect to idex in pinecone
pinecone_index = pinecone.Index("keyword-search")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="pg_essay_0.6.0")
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)


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
        for path in glob.glob(f"{files}/*"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                # Comparing the text of the node with the text of the response
                if reference in text:
                    Dict[path] = text
                    key.append(path)

    # getting url of the reference
    with open("URL.json") as f:
        d = json.load(f)
        # Searching for the url of the reference from dict of urls
        keys = next(
            (k for k, v in d.items() if v == (re.sub(r"\..*\/", "", key[0]).rstrip(".txt")).split("\\")[-1]), None
        )

    return keys, d[keys]


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query from url
        parsed_path = urlparse(self.path)
        query = str(parsed_path.query).strip("q=")
        encoded_text = unquote(query)

        # Get answer from query
        url, title = get_query(encoded_text)

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        # Display query
        self.wfile.write(f"question: {encoded_text}".encode("utf-8"))
        self.wfile.write(f"\n".encode("utf-8"))
        self.wfile.write(f"Url: {url}, Title: {title}".encode("utf-8"))
        return


reference, answer = get_query("√18(20-n)を自然数")

time_finish = time.time()


print(reference)
print(answer)

print(time_finish - time_start)
