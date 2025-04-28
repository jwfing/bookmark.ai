from utils.webpage_downloader import WebPageDownloader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

class Indexing:
    def __init__(self, vector_store: Chroma):
        self.downloader = WebPageDownloader()
        self.vector_store = vector_store
        pass

    async def index(self, url : str):
        docs = await self.downloader.download(url)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
        all_splits = text_splitter.split_documents(docs)
        self.vector_store.add_documents(all_splits)