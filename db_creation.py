import os
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_chroma import Chroma
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import getpass
import os

pdf_folder = "../mylife/mylife"
CHROMA_DB_DIR = "contracts_db"

embeddings = GPT4AllEmbeddings()
chroma_client = chromadb.PersistentClient(CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection(name="contracts",)

vector_store_from_client = Chroma(
    client=chroma_client,
    collection_name="contracts",
    embedding_function=embeddings,
)


def single_loader(pdf_folder: str, chunk_size: int, chunk_overlap: int):
    """Split pdf files into chunks and create embeddings"""

    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = chunk_overlap,
            )

    for sub_folder in os.listdir(pdf_folder):

        for pdf_file in os.listdir(os.path.join(pdf_folder, sub_folder)):

            if pdf_file.endswith(".pdf") or pdf_file.endswith(".PDF"):
                print(pdf_file)
                loader = PyPDFLoader(os.path.join(pdf_folder, sub_folder, pdf_file))
                docs = loader.load_and_split(text_splitter)
                metadata = [{"contract_number": sub_folder, "pdf_file": pdf_file} for _ in docs]
                ids = [sub_folder+"_"+str(i) for i in range(len(docs))]
                texts = [chunk.page_content for chunk in docs]
                try:
                    Chroma.from_texts(texts,
                                      embeddings,
                                      ids = ids,
                                      metadatas=metadata,
                                      collection_name="contracts",
                                      persist_directory=CHROMA_DB_DIR)
                except:
                    print("Cannot read pdf file")

if __name__ == "__main__":
    single_loader(pdf_folder, 500, 100)
