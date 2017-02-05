# 跨站请求相关 请求信息=>标准请求结果
from .utils import timeup
import requests
import time


@timeup
def get_quote(lookup):
    query_urls = [
        'http://query2.finance.yahoo.com/v8/finance/chart/',
        'http://query1.finance.yahoo.com/v8/finance/chart/',
        'http://query2.finance.yahoo.com/v7/finance/chart/',
        'http://query1.finance.yahoo.com/v7/finance/chart/',
    ]
    # requests.adapters.DEFAULT_RETRIES = 5
    payload = {'interval':'1d', 'range':'1y'}
    lookup = requests.utils.requote_uri(lookup)  # URL-encode 基本等价于urllib.parse.quote()，功能更保险
    rs = 0
    for url in query_urls:
        with requests.session() as s:  # 遏制requests.exceptions.ConnectionError，Max retries exceeded...
            try:
                rs = s.get(url + '%s' % lookup, params=payload, timeout=0.5)  # 卡顿出现位置，添加timeout！
                print('Requesting finance yahoo with "%s"' % lookup)
            except requests.exceptions.ReadTimeout:
                print('Requesting finance yahoo with "%s" failed' % lookup)
        if rs:
            break
        # time.sleep(0.5)
    result = rs.json()
    return result
