import unittest
from unittest.mock import Mock, patch
from app.utils.htmlparser import HTMLParser
import requests
from bs4 import BeautifulSoup

class TestHTMLParser(unittest.TestCase):
    def setUp(self):
        """测试前的初始化工作"""
        self.parser = HTMLParser(timeout=5)
        self.test_url = "https://example.com"
        
        # 准备测试数据
        self.test_html = """
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test Description">
            </head>
            <body>
                <h1>Hello World</h1>
                <p>This is a test paragraph.</p>
                <div>
                    <p>Nested content</p>
                </div>
            </body>
        </html>
        """

    @patch('requests.get')
    def test_fetch_and_parse_basic(self, mock_get):
        """测试基本的网页获取和解析功能"""
        # 设置 mock response
        mock_response = Mock()
        mock_response.text = self.test_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # 执行测试
        raw_content, content = self.parser.fetch_and_parse(self.test_url)
        
        # 验证结果
        self.assertEqual(raw_content, self.test_html)
        self.assertIn("Hello World", content)
        self.assertIn("This is a test paragraph", content)
        self.assertIn("Nested content", content)
        
        # 验证 requests.get 被正确调用
        mock_get.assert_called_once_with(self.test_url, timeout=5)

    @patch('requests.get')
    def test_fetch_and_parse_empty_content(self, mock_get):
        """测试空内容的情况"""
        mock_response = Mock()
        mock_response.text = "<html><body></body></html>"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        raw_content, content = self.parser.fetch_and_parse(self.test_url)
        
        self.assertEqual(raw_content, "<html><body></body></html>")
        self.assertEqual(content, "")

    @patch('requests.get')
    def test_fetch_and_parse_network_error(self, mock_get):
        """测试网络错误的情况"""
        mock_get.side_effect = requests.RequestException("Network error")
        
        with self.assertRaises(requests.RequestException):
            self.parser.fetch_and_parse(self.test_url)

    @patch('requests.get')
    def test_fetch_and_parse_timeout(self, mock_get):
        """测试超时的情况"""
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        with self.assertRaises(requests.Timeout):
            self.parser.fetch_and_parse(self.test_url)

    @patch('requests.get')
    def test_fetch_and_parse_invalid_html(self, mock_get):
        """测试无效HTML的情况"""
        mock_response = Mock()
        mock_response.text = "Invalid HTML Content"
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        raw_content, content = self.parser.fetch_and_parse(self.test_url)
        
        self.assertEqual(raw_content, "Invalid HTML Content")
        self.assertEqual(content, "Invalid HTML Content")

    @patch('requests.get')
    def test_fetch_and_parse_http_error(self, mock_get):
        """测试HTTP错误的情况"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Client Error")
        mock_get.return_value = mock_response
        
        with self.assertRaises(requests.HTTPError):
            self.parser.fetch_and_parse(self.test_url)

if __name__ == '__main__':
    unittest.main()