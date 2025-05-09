from flask_restful import Resource, reqparse

class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}

class QueryAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('q', type=str, required=False, help='Search query')
        args = parser.parse_args()
        
        # 这里添加查询逻辑
        return {
            'query': args.get('q'),
            'results': []  # 这里返回查询结果
        }

from app.utils.llama_processor import LlamaProcessor
from app.utils.htmlparser import HTMLParser
from app.models import RawPage, PageVectorIndex, SessionLocal

class IngestionAPI(Resource):
    def __init__(self):
        self.llama_processor = LlamaProcessor()
        self.html_parser = HTMLParser()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True, help='URL is required')
        parser.add_argument('owner', type=str, required=True, help='Owner is required')
        args = parser.parse_args()
        print(args)
        
        try:
            # 使用 HTMLParser 获取和解析内容
            raw_content, content = self.html_parser.fetch_and_parse(args['url'])

            # output content to console
            print(args['url'], content)
            
            db = SessionLocal()
            
            # 保存原始页面
            raw_page = RawPage(
                owner=args['owner'],
                url=args['url'],
                content=content,
                raw_content=raw_content,
                status=0
            )
            db.add(raw_page)
            db.flush()
            
            # 处理并保存向量索引
            processed_chunks = self.llama_processor.process_content(
                content,
                metadata={'url': args['url'], 'owner': args['owner']}
            )
            
            for chunk in processed_chunks:
                # Convert embedding to flat list and ensure it's 1536 dimensions
                embedding_array = chunk['embedding'].flatten().tolist() if hasattr(chunk['embedding'], 'flatten') else chunk['embedding']
                if len(embedding_array) != 1536:
                    raise ValueError(f"Expected 1536 dimensions, got {len(embedding_array)}")
                
                vector_index = PageVectorIndex(
                    page_id=raw_page.id,
                    chunk_index=chunk['chunk_index'],
                    chunk_text=chunk['chunk_text'],
                    embedding=embedding_array,
                    meta_info=chunk['meta_info']
                )
                db.add(vector_index)
            
            db.commit()
            db.close()
            
            return {
                'status': 'success',
                'message': 'Page processed and indexed',
                'data': {
                    'url': args['url'],
                    'owner': args['owner'],
                    'chunks_count': len(processed_chunks)
                }
            }, 201
            
        except Exception as e:
            if 'db' in locals():
                db.close()
            return {
                'status': 'error',
                'message': f'Error: {str(e)}'
            }, 500

def init_api(api):
    api.add_resource(HelloWorld, '/api/hello')
    api.add_resource(QueryAPI, '/api/query')
    api.add_resource(IngestionAPI, '/api/ingestion')