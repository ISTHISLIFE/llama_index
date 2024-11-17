from llama_index.core import SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)





class llm:
    def __init__(self):
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
        Settings.llm = Ollama(model="llama3.1:latest", request_timeout=360.0)
        self.load()

    def load_document(self, path):
   
       # subfolders_with_files = []

        for root, dirs, files in os.walk(path):
            
            if files:  # Check if the current folder contains any files
              #  subfolders_with_files.append(root)
                print(dirs)
                documents = SimpleDirectoryReader(root).load_data()
                update_index = VectorStoreIndex.from_documents(documents)
                update_index.storage_context.persist(persist_dir="./storage")
        self.load()
        print("done")

  
   
   
   
    def load(self): 
        # data_finder is class object to extract relevant data 
        # data_finder.find() = vector_store, storage_context 
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
        retriever = VectorIndexRetriever(
                index=index,

                similarity_top_k=10
            )


        response_synthesizer = get_response_synthesizer()

        self.query_engine = index.as_query_engine()

    
        
   
   


 

    def inference(self, input):
        response = self.query_engine.query(input)
        print(response)
        return response

