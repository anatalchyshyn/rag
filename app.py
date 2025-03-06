from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_mistralai import MistralAIEmbeddings
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langchain_community.embeddings import GPT4AllEmbeddings
import os

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

embeddings = GPT4AllEmbeddings()
vector_store = Chroma(collection_name="rag_model",
                      persist_directory="./chroma_langchain_db",
                      embedding_function = embeddings)


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state['question'], k = 3)
    return {"context": retrieved_docs}

question = ""
result = retrieve(question)
print(result)

##########

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

query = ""
response = rag_chain.invoke({"input": query})
print(response["answer"])
