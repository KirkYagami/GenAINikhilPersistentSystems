

import PyPDF2
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions



default_ef = embedding_functions.DefaultEmbeddingFunction()


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
def create_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def store_in_chromadb(chunks, collection_name="pdf_chunks"):
    client = chromadb.Client()

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=default_ef
    )
    

    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({"source": "pdf", "chunk_id": i})
        ids.append(f"chunk_{i}")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return collection


def process_pdf(pdf_path, collection_name="pdf_chunks"):

    text = extract_text_from_pdf(pdf_path)
    
    chunks = create_chunks(text)
    print(f"Created {len(chunks)} chunks from the PDF")

    collection = store_in_chromadb(chunks, collection_name)
    print(f"Stored chunks in ChromaDB collection: {collection_name}")
    
    return collection

if __name__ == "__main__":
    pdf_path = "1706.03762v7.pdf"
    collection = process_pdf(pdf_path)

    results = collection.query(
        query_texts=["How does the encoder decoder architecture work?"],
        n_results=3
    )
    print("Query results:", results)