import pinecone 
from langchain.vectorstores import Pinecone
import utils


documents = utils.loadData()
print(len(documents))

docs = utils.split_docs(documents)

from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# initialize pinecone
pinecone.init(
    api_key="",  # find at app.pinecone.io
    environment="us-east4-gcp"  # next to api key in console
)

index_name = "langchain-chatbot"

index = Pinecone.from_documents(docs, embeddings, index_name=index_name)