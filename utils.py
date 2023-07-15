from langchain.document_loaders import DirectoryLoader
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

def getResponse(query):
    return "hello"+query

def loadData():
    directory = 'data/testdata.json'
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

# documents = load_docs(directory)
# len(documents)


def split_docs(documents,chunk_size=500,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs




def get_similiar_docs(query, k=1, score=False):
  if score:
    similar_docs = index.similarity_search_with_score(query,k=k)
  else:
    similar_docs = index.similarity_search(query,k=k)
  return similar_docs

# docs = split_docs(documents)
# print(len(docs))