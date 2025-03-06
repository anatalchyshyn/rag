from langchain_community.document_loaders import PyPDFLoader, PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
import os

def folder_loader(filepath: str):

    loader = PyPDFDirectoryLoader(filepath)
    docs = loader.load()
    return docs

def single_loader(pdf_folder: str, chunk_size: int, chunk_overlap: int):
    # split pdf files into chunks and create embeddings
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            )

    documents = []

    for sub_folder in os.listdir(pdf_folder):
        for pdf_file in os.listdir(os.path.join(pdf_folder, sub_folder)):

            if pdf_file.endswith(".pdf") or pdf_file.endswith(".PDF"):

                loader = PyPDFLoader(os.path.join(pdf_folder, sub_folder, pdf_file))
                docs = loader.load_and_split(text_splitter)
                documents.extend(docs)

        if len(documents) > 5:
            return documents
    return documents

if __name__ == "__main__":

    documents = single_loader("files/mylife", 300, 50)
    print("Documents readed")
    print("Example:")
    print(documents[0])
    embeddings = GPT4AllEmbeddings()
    vector_store = Chroma(collection_name="rag-model",
                      persist_directory="./chroma_langchain_db",
                      embedding_function=embeddings)
    vector_store.add_documents(documents)
    print("Successfully created vector DB")