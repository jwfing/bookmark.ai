import requests
from bs4 import BeautifulSoup
from typing import Dict, Tuple

class HTMLParser:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch_and_parse(self, url: str) -> Tuple[str, str]:
        """
        获取并解析网页内容
        
        Args:
            url: 网页URL
            
        Returns:
            Tuple[str, str]: (原始内容, 处理后的文本内容)
            
        Raises:
            requests.RequestException: 当网页获取失败时
        """
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        raw_content = response.text
        
        # 解析HTML
        soup = BeautifulSoup(raw_content, 'html.parser')
        content = ' '.join([text for text in soup.stripped_strings])
        
        return raw_content, content

    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        提取页面元数据（如标题、描述等）
        """
        metadata = {}
        
        # 提取标题
        title = soup.find('title')
        if title:
            metadata['title'] = title.string
            
        # 提取描述
        description = soup.find('meta', {'name': 'description'})
        if description:
            metadata['description'] = description.get('content', '')
            
        return metadata