from chalice import Chalice
import tda
from tda import auth, client
from chalicelib import config
import os

app = Chalice(app_name='tda')


@app.route('/')
def index():
    token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    c = auth.client_from_token_file(token_path, config.api_key)
    r=c.get_quote("PLTR")
    return r.json()
    # return {'hello': 'world'}


@app.route('/order',methods=["POST"])
def order():
    webhook=app.current_request.json_body
    print(webhook)
    name=webhook["ticker"].upper()
    token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    c = auth.client_from_token_file(token_path, config.api_key)
    order_limit = tda.orders.equities.equity_buy_limit(name, price=webhook["close"],quantity=5)
    r = c.place_order(config.account_id, order_limit)
    if r :
        print("=====")
        print("Limit Order : "+f'{name}')

    return {
        "status":"success",
        "message":webhook,
        "ticker":webhook["ticker"]
    }
    


