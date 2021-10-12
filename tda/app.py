from chalice import Chalice
import tda
from tda import auth, client
from chalicelib import config
import os,json

app = Chalice(app_name='tda')
app.debug = True

init =False


def mkdir():
    global init 
    
    if not init:
        token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')

        f = open(token_path,"r")
        doc = json.load(f)
        f.close()

        f2 = open("/tmp/token","w")
        json.dump(doc,f2)
        f2.close()

        init = True

@app.route('/')
def index():
    # token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    # c = auth.client_from_token_file(token_path, config.api_key)
    mkdir()
    c = auth.client_from_token_file("/tmp/token", config.api_key)
    r=c.get_quote("GOOGL")
    return r.json()

@app.route('/order',methods=["POST"])
def order():
    # token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    # c = auth.client_from_token_file(token_path, config.api_key)
    webhook=app.current_request.json_body
    name=webhook["ticker"].upper()
    mkdir()

    if float(webhook["close"])>100:
        num=1
    else:
        num=int(100/float(webhook["close"]))

    c = auth.client_from_token_file("/tmp/token", config.api_key)
    order_limit = tda.orders.equities.equity_buy_limit(name, price=webhook["close"],quantity=num)
    r = c.place_order(config.account_id, order_limit)

    if r :
        print("=====")
        print("Buy Limit Order : "+f'{name}')

    return {
        "Status":"Success",
        "Message":webhook
    }

@app.route('/sell',methods=["POST"])
def sell():
    # token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    # c = auth.client_from_token_file(token_path, config.api_key)
    webhook=app.current_request.json_body
    name=webhook["ticker"].upper()
    mkdir()
    if float(webhook["close"])>100:
        num=1
    else:
        num=int(100/float(webhook["close"]))
    c = auth.client_from_token_file("/tmp/token", config.api_key)
    sell_order_market = tda.orders.equities.equity_sell_market(name,quantity=num)
    r = c.place_order(config.account_id, sell_order_market)

    if r :
        print("=====")
        print("Sell Market Order : "+f'{name}')

    return {
        "Status":"success",
        "Message":webhook
    }





