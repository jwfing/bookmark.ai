from utils.webpage_downloader import WebPageDownloader
import pytest

@pytest.mark.asyncio
async def test_download_webpage():
    page_url = "https://python.langchain.com/docs/how_to/chatbots_memory/"
    downloader = WebPageDownloader()
    html = await downloader.download(page_url)
    assert len(html) > 0
    print(html[0].page_content)