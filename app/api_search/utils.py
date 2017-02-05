# 其他

from bson import json_util, ObjectId  # bson模块解析
import json

import functools
import time


def bson_to_json(data):  # bson、字典=>json
    return json.dumps(data, default=json_util.default)


def bson_obj_id(id):  # 构造供id查询
    return ObjectId(id)


def timeup(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.clock()
        result = fn(*args, **kwargs)
        end = time.clock()
        print('It takes %.3f sec to get the data from yahoo.' % (end - start))
        return result
    return wrapper