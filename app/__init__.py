from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask import Flask
import os

bootstrap = Bootstrap()
mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    # 为该app挂载各种与该模块相关的配置.config 与 属性方法等
    # app.config['MONGO_URI'] = 'mongodb://localhost/quote_lookup'
    app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME') or 'quote_lookup'
    app.config['MAIL_ADMIN'] = os.environ.get('MAIL_ADMIN') or 'cwr603@126.com'

    bootstrap.init_app(app)
    mongo.init_app(app)


    # blueprint注册
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api_search import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app