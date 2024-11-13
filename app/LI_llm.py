from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor






class LI_llm:
    def __init__(self):
        Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

        Settings.llm = Ollama(model="llama3.1:latest", request_timeout=360.0)
        

    def load(self): 
        # data_finder is class object to extract relevant data 
        # data_finder.find() = vector_store, storage_context 
        documents = SimpleDirectoryReader("data").load_data()
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )

        self.query_engine = index.as_query_engine()
        retriever = VectorIndexRetriever(
            index=index,
            similarity_top_k=10,
        )

    # configure response synthesizer
        response_synthesizer = get_response_synthesizer()

    # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
        )

    def inference(self, input):
        self.load()
        response = self.query_engine.query("What did the author do growing up?")
        return response
    

model = llama_index_llm()
out = model.inference("what is a peony flower?")
print(out) 