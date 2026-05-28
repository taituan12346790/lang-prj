from app.rag.vector_store import VectorStore
from app.rag.df_retriever_lite import DF_Retriever_Lite


def initialize_retriever():
    store = VectorStore()
    store.load()

    if store.index is None:
        return None

    return DF_Retriever_Lite(
        faiss_index=store.index,
        id_to_chunk=store.metadata
    )