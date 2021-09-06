import requests,json
from config import * 
url="https://paper-api.alpaca.markets"

account_url="{}/v2/account".format(url)
order_url="{}/v2/orders".format(url)
head={"APCA-API-KEY-ID":APIKEY,"APCA-API-SECRET-KEY":APISECRET}


def get():
    r=requests.get(account_url, headers=head)
    return json.loads(r.content)

def order(symbol,qty,side,type,time):
    data={
        "symbol":symbol,
        "qty":qty,
        "side":side,
        "type":type,
        "time_in_force":time
    }
    r=requests.post(order_url,json=data,headers=head)
    return json.loads(r.content)


ORDER=order("AAPL",1,"buy","market","gtc")
print(ORDER)