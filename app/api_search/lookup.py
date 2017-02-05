from . import api
from .requests_cross import get_quote
from .data_parser import resolve_quote
from .utils import bson_to_json
from .errors import not_found
from .. import mongo
from flask import request
import time, datetime


@api.route('/results')
def index():  # 获取GET查询请求，json返回页面内容解析数据
    lookup = request.args.get('lookup', 'GOOG').upper()
    quote_information_in_db = mongo.db.quote.find_one({'symbol': lookup})  # return Dict对象

    # 查询逻辑
    # if quote_information_in_db and (datetime.datetime.now().day == datetime.date.fromtimestamp(quote_information_in_db.get('last_update', 0)).day):  # 隔天更新
    if quote_information_in_db and (time.time() - quote_information_in_db.get('last_update', 0) <= 60 * 60 * 8):  # 8小时更新
        print('Get "%s" data directly from database.' % lookup)
        mongo.db.quote.update_one({'symbol': lookup}, {'$inc': {'request_times':1}})
        results = mongo.db.quote.find_one({'symbol': lookup})
        quote_results = {
            'error': None,
            'results': results
        }
        return bson_to_json(quote_results)
    lookup_ans = get_quote(lookup)

    # 错误处理
    if not lookup_ans['chart']['result']:
        return not_found('抱歉！未能找到%s相关Quote信息。' % lookup)

    # 解析结果
    quote_information = resolve_quote(quote_information_in_db, lookup_ans)

    # 并更新到数据库
    if quote_information_in_db:
        mongo.db.quote.update_one(quote_information_in_db, {'$set':quote_information})
    else:
        mongo.db.quote.insert_one(quote_information).inserted_id

    quote_results = {
        'error': None,
        'results':quote_information
    }
    return bson_to_json(quote_results)



