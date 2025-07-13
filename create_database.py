from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

import os
import shutil

from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import openai
from dotenv import load_dotenv


# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()
#---- Set OpenAI API key 
# Change environment variable name from "OPENAI_API_KEY" to the name given in 
# your .env file.
openai.api_key = os.environ['OPENAI_API_KEY']

DATA_PATH = "data/books"
CHROMA_PATH = "chroma"

def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)



# 讀取檔案
def load_documents():
    loader = PyPDFDirectoryLoader(DATA_PATH, glob="*.pdf")
    documents = loader.load()
    return documents

# 分割檔案
def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function = len,
        add_start_index = False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[3]
    print(document.page_content)
    print(document.metadata)

    return chunks

# 用 OPENAI 的 Embeddings 方法把檔案轉成 vectorDB
def save_to_chroma(chunks: list[Document]):
    # 清除舊的 database
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # 建一個新的 database
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()