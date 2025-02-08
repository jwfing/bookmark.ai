from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    api = Api(app)
    
    # 导入和注册路由
    from app.api import routes
    routes.init_api(api)
    
    return app