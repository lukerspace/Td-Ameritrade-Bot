from chalice import Chalice
import tda
from tda import auth, client
from chalicelib import config
import os,json

app = Chalice(app_name='tda')
app.debug = True


# Mark When Deploy Only 
init =False

# for the tda api will repeatedly create token for we dont need this funtion 
# mark down the line 30,31 in auth.py
# load the token once in chalicelib and rewrite it in tmp/token

def mkdir_in_tmp():
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
    
    # DEBUG IN LOCAL
    # token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    # c = auth.client_from_token_file(token_path, config.api_key)
    
    # MARK WHEN DEPLOY
    mkdir_in_tmp()
    c = auth.client_from_token_file("/tmp/token", config.api_key)
    r=c.get_quote("GOOGL")
    return r.json()

@app.route('/order',methods=["POST"])
def order():
    # DEBUG IN LOCAL
    # token_path=os.path.join(os.path.dirname(__file__),"chalicelib",'token')
    # c = auth.client_from_token_file(token_path, config.api_key)

    # RECEIVE THE WEBHOOK REQUEST
    webhook=app.current_request.json_body
    name=webhook["ticker"].upper()
    
    # MARK WHEN DEPLOY
    mkdir_in_tmp()
    if webhook["side"]=="buy":
        if float(webhook["close"])>100:
            num=1
        else:
            num=int(100/float(webhook["close"]))
        # DEPLOY
        c = auth.client_from_token_file("/tmp/token", config.api_key)
        order_limit = tda.orders.equities.equity_buy_limit(name, price=webhook["close"],quantity=num)
        r = c.place_order(config.account_id, order_limit)

        if r :
            print("Buy Limit Order : "+f'{name}')

        return {
            "Status":"Success",
            "Message":webhook
        }

    if webhook["side"]=="sell":
        if float(webhook["close"])>100:
            num=1
        else:
            num=int(100/float(webhook["close"]))
        # DEPLOY
        c = auth.client_from_token_file("/tmp/token", config.api_key)
        sell_order_market = tda.orders.equities.equity_sell_market(name,quantity=num)
        r = c.place_order(config.account_id, sell_order_market)

        if r :
            print("Sell Market Order : "+f'{name}')

        return {
            "Status":"success",
            "Message":webhook
        }

