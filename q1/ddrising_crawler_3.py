from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import json


def get_history_data(s_dateStr,e_datestr):
    target_url_2 = "https://cn.investing.com/instruments/HistoricalDataAjax"
    
    headers = {'Accept': 'text/plain, */*; q=0.01', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0','X-Requested-With':'XMLHttpRequest'}
    ses = requests.Session()
    res = ses.get('https://cn.investing.com/equities/apple-computer-inc-historical-data', headers=headers, timeout=60)
    ses.headers.update(headers)
    res.encoding = 'utf-8'
    rows = res.text.split("\n")
    print("Rows: {}".format(len(rows)))
    target_idx = -1
    for idx, row in enumerate(rows):
        row =row.strip()
        if row.startswith("window.histDataExcessInfo") and target_idx==-1:
            target_idx = idx
            break
    
    curr_id = int(rows[target_idx+1].strip()[8:len(rows[target_idx+1].strip())-1])
    smlID = int(rows[target_idx+2].strip()[7:-5])    
    print("Get cuur_id:{}, smlID:{}".format(curr_id,smlID))

    #payload = urlencode({"curr_id":str(curr_id),"smlID":str(smlID),"header":"AAPL历史数据","st_date":"2021/12/20","end_date":"202/01/19","interval_sec":"Daily","sort_col":"date","sort_ord":"DESC","action":"historical_data"})
    payload = {"curr_id":str(curr_id),"smlID":str(smlID),"header":"AAPL%E5%8E%86%E5%8F%B2%E6%95%B0%E6%8D%AE","st_date":s_dateStr,"end_date":e_datestr,"interval_sec":"Daily","sort_col":"date","sort_ord":"DESC","action":"historical_data"}
    print(payload)
    headers = {'X-Requested-With':'XMLHttpRequest'}
    post_res  = ses.post(target_url_2, data = payload, headers = headers)
    post_res.encoding = 'utf-8'
    '''
    with open("c:/temp/output.txt",'w',encoding="utf-8") as fp:
        fp.write(post_res.text)
    '''
    result = []
    soup = BeautifulSoup(post_res.text,"lxml")
    rows = soup.tbody.find_all("tr")
    for idx, row in enumerate(rows):
        tds = row.find_all("td")
        data_row = {"日期":tds[0].text,"收盘":tds[1].text,"开盘":tds[2].text,"高":tds[3].text,"低":tds[4].text,"交易量":tds[5].text,"涨跌幅":tds[6].text}
        result.append(data_row)
    return json.dumps(result)

ses = None
if __name__=="__main__":
    print(get_history_data("2021/12/20","2022/01/20"))