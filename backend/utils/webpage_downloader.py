import bs4
from langchain_community.document_loaders import WebBaseLoader

class WebPageDownloader:
    def __init__(self):
        pass
    async def download(self, url):
        loader = WebBaseLoader(web_paths=[url])
        docs = []
        async for doc in loader.alazy_load():
            docs.append(doc)
        return docs
