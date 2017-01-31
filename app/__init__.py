from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask import Flask

bootstrap = Bootstrap()
mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    # app.config['MONGO_URI'] = 'mongodb://localhost/quote_lookup'
    app.config['MONGO_DBNAME'] = 'quote_lookup'
    # 为该app挂载各种与该模块相关的配置.config 与 属性方法等
    bootstrap.init_app(app)
    mongo.init_app(app)


    # blueprint注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_search import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app