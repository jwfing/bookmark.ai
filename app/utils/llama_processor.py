from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
from app.utils.embedding_factory import get_embedding_model
from app.config import Config 
import json

class LlamaProcessor:
    def __init__(self):
        self.node_parser = SimpleNodeParser.from_defaults(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        self.embed_model = get_embedding_model()
    
    def process_content(self, content, metadata=None):
        # 创建文档对象
        doc = Document(text=content, metadata=metadata or {})
        
        # 分块处理
        nodes = self.node_parser.get_nodes_from_documents([doc])
        
        # 生成向量嵌入
        results = []
        for idx, node in enumerate(nodes):
            text = node.get_content()
            embedding_result = self.embed_model.get_text_embedding(text)
            
            # 从 numpy.ndarray 转换为 Python 字典
            embedding_dict = embedding_result.item()
            
            # 获取向量数据
            embedding_vector = embedding_dict['embedding']
            
            # 确保 metadata 不为 None
            meta = metadata or {}
            
            results.append({
                'chunk_index': idx,
                'chunk_text': text,
                'embedding': embedding_vector,
                'meta_info': json.dumps({
                    'source': meta.get('url', ''),
                    'chunk_size': len(text),
                    'position': idx
                })
            })
        
        return results