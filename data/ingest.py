from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

print("Loading documents...")
loader = DirectoryLoader("data/docs", glob="**/*.md")
docs = loader.load()

print(f"{len(docs)} documents loaded")

embeddings = OpenAIEmbeddings()
vectorstores = FAISS.from_documents(docs, embeddings)

vectorstores.save_local("data/index")
print("Vector index saved to data/index")