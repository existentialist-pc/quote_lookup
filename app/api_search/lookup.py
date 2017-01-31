from . import api
from .requests_cross import get_quote_from_yahoo
from flask import request
from .. import mongo
from bson import json_util, ObjectId  # bson自带库
import time
import json
import logging


def bson_to_json(data):  # bson、字典=>json
    return json.dumps(data, default=json_util.default)


def bson_obj_id(id):  # 构造供id查询
    return ObjectId(id)


@api.route('/results')
def index():  # 获取GET查询请求，json返回页面内容解析数据
    lookup = request.args.get('lookup', 'GOOG').upper()
    information_in_db = mongo.db.quote.find_one({'symbol': lookup})  # return Dict对象

    # 查询逻辑
    if information_in_db and (time.time() - information_in_db.get('last_update', 0) <= 86400):  # 更新<24小时
        # print('Get "%s" data directly from database.' % lookup)
        mongo.db.quote.update_one({'symbol': lookup}, {'$inc': {'request_times':1}})
        results = mongo.db.quote.find_one({'symbol': lookup})
        return bson_to_json(results)
    ans = get_quote_from_yahoo(lookup)

    # 解析数据
    # 关心数据有chart=>error,result[0]=>timestamp、meta、indicators['quote']的[0]['open'] ... high volume close low
    # 未修正数据在 indicators下的['unadjquote']['unadjopen'] unadjhigh unadjlow等等 与 ['unadjclose']['unadjclose']
    information = ans['chart']['result'][0]['indicators']['quote'][0].copy()  # open high low close volume
    symbol = ans['chart']['result'][0]['meta']['symbol']
    timestamp = ans['chart']['result'][0]['timestamp']
    last_update = time.time()
    request_times = 1 + information_in_db.get('request_times', 1) if information_in_db else 1

    # 更新逻辑
    information.update({
        'symbol':symbol,
        'timestamp':timestamp,
        'request_times':request_times,
        'last_update':last_update,
    })

    if information_in_db:
        mongo.db.quote.update_one(information_in_db, {'$set':information})
    else:
        mongo.db.quote.insert_one(information).inserted_id
    results = mongo.db.quote.find_one({'symbol': lookup})
    return bson_to_json(results)



