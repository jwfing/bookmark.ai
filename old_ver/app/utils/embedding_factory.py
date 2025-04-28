from dashscope import TextEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from app.config import Config
import numpy as np

class QwenEmbedding:
    def __init__(self):
        self.api_key = Config.DASHSCOPE_API_KEY

    def get_text_embedding(self, text):
        response = TextEmbedding.call(
            model='text-embedding-v2',
            input=text,
            api_key=self.api_key
        )
        if response.status_code == 200:
            return np.array(response.output['embeddings'][0])
        else:
            raise Exception(f"Error getting embedding: {response.message}")

def get_embedding_model():
    if Config.EMBEDDING_MODEL == 'qwen':
        return QwenEmbedding()
    else:
        return OpenAIEmbedding(api_key=Config.OPENAI_API_KEY)