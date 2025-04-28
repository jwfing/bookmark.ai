import unittest
from unittest.mock import Mock, patch
import json
import numpy as np
from app.utils.llama_processor import LlamaProcessor
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser

class TestLlamaProcessor(unittest.TestCase):
    @patch('app.utils.llama_processor.Config')
    def setUp(self, mock_config):
        """测试前的初始化工作"""
        # 设置 Config mock
        mock_config.CHUNK_SIZE = 1024
        mock_config.CHUNK_OVERLAP = 50
        
        self.processor = LlamaProcessor()
        
        # Mock node_parser
        self.processor.node_parser = Mock(spec=SimpleNodeParser)
        
        # Mock embed_model
        self.processor.embed_model = Mock()
        
        # 准备测试数据
        self.test_content = "This is a test content."
        self.test_metadata = {
            "url": "https://example.com",
            "title": "Test Page"
        }
        
        # 模拟的向量嵌入
        self.mock_embedding = np.array([0.1, 0.2, 0.3])

    def test_process_content_basic(self):
        """测试基本的内容处理功能"""
        # 设置 mock 的返回值
        mock_node = Mock()
        mock_node.get_content.return_value = self.test_content
        self.processor.node_parser.get_nodes_from_documents.return_value = [mock_node]
        self.processor.embed_model.get_text_embedding.return_value = self.mock_embedding
        
        # 执行测试
        results = self.processor.process_content(self.test_content, self.test_metadata)
        
        # 验证结果
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['chunk_index'], 0)
        self.assertEqual(results[0]['chunk_text'], self.test_content)
        self.assertTrue(np.array_equal(results[0]['embedding'], self.mock_embedding))
        
        # 验证 meta_info
        meta_info = json.loads(results[0]['meta_info'])
        self.assertEqual(meta_info['source'], self.test_metadata['url'])
        self.assertEqual(meta_info['position'], 0)
        self.assertEqual(meta_info['chunk_size'], len(self.test_content))

    def test_process_content_multiple_chunks(self):
        """测试处理多个文本块的情况"""
        # 准备多个模拟的文本块
        mock_nodes = [Mock(), Mock()]
        mock_nodes[0].get_content.return_value = "Chunk 1"
        mock_nodes[1].get_content.return_value = "Chunk 2"
        
        self.processor.node_parser.get_nodes_from_documents.return_value = mock_nodes
        self.processor.embed_model.get_text_embedding.return_value = self.mock_embedding
        
        # 执行测试
        results = self.processor.process_content(self.test_content, self.test_metadata)
        
        # 验证结果
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['chunk_index'], 0)
        self.assertEqual(results[1]['chunk_index'], 1)
        self.assertEqual(results[0]['chunk_text'], "Chunk 1")
        self.assertEqual(results[1]['chunk_text'], "Chunk 2")

    def test_process_content_no_metadata(self):
        """测试没有提供元数据的情况"""
        mock_node = Mock()
        mock_node.get_content.return_value = self.test_content
        self.processor.node_parser.get_nodes_from_documents.return_value = [mock_node]
        self.processor.embed_model.get_text_embedding.return_value = self.mock_embedding
        
        # 执行测试，不提供 metadata
        results = self.processor.process_content(self.test_content)
        
        # 验证结果
        self.assertEqual(len(results), 1)
        meta_info = json.loads(results[0]['meta_info'])
        self.assertEqual(meta_info['source'], '')  # 应该是空字符串
        
    def test_process_content_empty_content(self):
        """测试空内容的情况"""
        # 模拟空内容的处理
        self.processor.node_parser.get_nodes_from_documents.return_value = []
        
        # 执行测试
        results = self.processor.process_content("")
        
        # 验证结果
        self.assertEqual(len(results), 0)
        
    def test_process_content_embedding_error(self):
        """测试嵌入生成失败的情况"""
        mock_node = Mock()
        mock_node.get_content.return_value = self.test_content
        self.processor.node_parser.get_nodes_from_documents.return_value = [mock_node]
        
        # 模拟嵌入生成失败
        self.processor.embed_model.get_text_embedding.side_effect = Exception("Embedding failed")
        
        # 验证异常抛出
        with self.assertRaises(Exception):
            self.processor.process_content(self.test_content)

if __name__ == '__main__':
    unittest.main()