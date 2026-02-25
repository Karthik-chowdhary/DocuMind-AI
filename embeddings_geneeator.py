from cli import LoadModelProgress
loader = LoadModelProgress()
_model_class = loader.start()
import fitz
import re
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

def embedd(pdf_path):
    embedding_model = _model_class(model_name = "all-MiniLM-L6-v2")
    cdir = os.getcwd()
    pdf_dir = os.path.join(cdir,"available_pdfs.json")
    with open(pdf_dir,'r') as file:
        data = json.load(file)
    file_name = os.path.basename(pdf_path)
    name,ext = os.path.splitext(file_name)
    
    if name in data:
        print("\nError: selected file already exist in data bases\n")
        return
    
    doc = fitz.open(pdf_path)
    full_text = ""
    
    for page_num,page in enumerate(doc):
        text = page.get_text()
        full_text += f"\n----------page: {page_num + 1} ------------\n"
        full_text += text
    doc.close()
    
    clean_text = re.sub(r'(\w+)-\n(\w+)',r'\1\2',full_text)
    clean_text = re.sub(r'\s+',' ',clean_text).strip()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len,
    ) 
    chunks = splitter.create_documents([clean_text])
    
    
    cdir = os.getcwd()
    folder_path = os.path.join(cdir,"vector_data_base's")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    
    base_dir = "./"
    dir = os.path.join(base_dir,folder_path,f"{name}_db{ext}")
    
    
    data.append(name)
    with open(pdf_dir,'w') as file:
        json.dump(data,file)
    
    
    from langchain_chroma import Chroma
    vector_db = Chroma.from_documents(
        documents = chunks,
        persist_directory = dir,
        embedding= embedding_model
    )
    
    return vector_db

def load_existing_db(pdf_name):
    embedding_model = _model_class(model_name = "all-MiniLM-L6-v2")
    base_dir = "./"
    cdir = os.getcwd()
    folder_path = os.path.join(cdir,"vector_data_base's")
    dir = os.path.join(base_dir,folder_path,f"{pdf_name}_db.pdf")
    
    from langchain_chroma import Chroma
    vector_db = Chroma(
        persist_directory= dir,
        embedding_function= embedding_model,
    )
    return vector_db
