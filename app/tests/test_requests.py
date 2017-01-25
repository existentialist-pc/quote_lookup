import requests
from bs4 import BeautifulSoup


lookup = input("输入代码：")

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
}
rs = requests.get('https://finance.yahoo.com/quote/%s/history?p=%s' % (lookup,lookup), headers=headers)
ans = rs.text
print(ans)
ans_bs = BeautifulSoup(ans, 'lxml')
historical_prices = ans_bs.findAll('table', {'class':'W(100%) M(0) BdB Bdc($lightGray)'})[0].findAll('tr')
print(historical_prices)