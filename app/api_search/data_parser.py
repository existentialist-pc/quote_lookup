# 请求数据解析相关 标准请求结果=>所需储存field格式
import time


def resolve_quote(quote_information_in_db, ans):  # 从原始dict提取所需dict数据返回，构建collection：quote的field

    '''  # 自用可删除
    关心数据有chart=>error,result[0]=>timestamp、meta、indicators['quote']的[0]['open'] ... high volume close low
    未修正数据在 indicators下的['unadjquote']['unadjopen'] unadjhigh unadjlow等等 与 ['unadjclose']['unadjclose']
    '''

    information = ans['chart']['result'][0]['indicators']['quote'][0].copy()  # 获得open high low close volume
    symbol = ans['chart']['result'][0]['meta']['symbol']
    timestamp = ans['chart']['result'][0]['timestamp']
    last_update = time.time()
    request_times = 1 + quote_information_in_db.get('request_times', 1) if quote_information_in_db else 1

    information.update({
        'symbol': symbol,
        'timestamp': timestamp,
        'request_times': request_times,
        'last_update': last_update,
    })
    return information
