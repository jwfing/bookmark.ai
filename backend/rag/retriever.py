from langchain_chroma import Chroma
from langchain import hub
from rag.data_source import llm

class Retriever:
    def __init__(self, vector_store: Chroma):
        self.vector_store = vector_store
        self.prompt = hub.pull("rlm/rag-prompt")

    def retrieve_and_generate(self, query: str):
        retrieve_docs = self.vector_store.similarity_search(query, k=3)
        if len(retrieve_docs) == 0:
            return "No relevant documents found."
        docs_content = "\n--------\n".join(doc.page_content for doc in retrieve_docs)
        messages = self.prompt.invoke({"question": query, "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}
