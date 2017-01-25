# 跨站请求相关
import requests


def get_quote_from_yahoo(lookup):
    query_urls = [
        'http://query2.finance.yahoo.com/v8/finance/chart/',
        'http://query1.finance.yahoo.com/v8/finance/chart/',
        'http://query2.finance.yahoo.com/v7/finance/chart/',
        'http://query1.finance.yahoo.com/v7/finance/chart/',
    ]
    # requests.adapters.DEFAULT_RETRIES = 5
    for url in query_urls:
        with requests.session() as s:  # 遏制requests.exceptions.ConnectionError，Max retries exceeded...
            rs = s.get(url + '%s' % lookup)
        if rs:
            break
    result = rs.json()
    return result