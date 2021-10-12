import config
import time ,urllib,requests,json
from splinter import Browser

import tda
from tda import *
from tda.orders.equities import *

def authenticate():
    try:
        c = auth.client_from_token_file(config.token_path, config.api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
            c = auth.client_from_login_flow(
                driver, config.api_key, config.redirect_uri, config.token_path)
    return c

def authenticate_auto():
    executable_path = {'executable_path': config.chromedriver_path}
    # Create a new instance of the browser, make sure we can see it (Headless = False)
    browser = Browser('chrome', **executable_path, headless=False)
    # define the components to build a URL
    method = 'GET'
    url = 'https://auth.tdameritrade.com/auth?'
    client_code = config.client_id + '@AMER.OAUTHAP'
    payload = {'response_type':'code', 'redirect_uri':'http://localhost/test', 'client_id':client_code}
    # build the URL and store it in a new variable
    p = requests.Request(method, url, params=payload).prepare()
    myurl = p.url
    # go to the URL
    browser.visit(myurl)
    # define items to fillout form
    payload = {'username': config.account_number,
            'password': config.password}
    # fill out each part of the form and click submit
    username = browser.find_by_id("username0").first.fill(payload['username'])
    password = browser.find_by_id("password1").first.fill(payload['password'])
    submit   = browser.find_by_id("accept").first.click()
    # click the Accept terms button
    browser.find_by_id("accept").first.click() 
    # give it a second, then grab the url
    time.sleep(1)
    new_url = browser.url
    # grab the part we need, and decode it.
    parse_url = urllib.parse.unquote(new_url.split('code=')[1])
    print(parse_url)
    # close the browser
    browser.quit()
    return "done"


def order(c):
    name="PLTR"
    market=c.get_quote(name)
    marketInfo=market.json()
    order_limit = tda.orders.equities.equity_buy_limit(name, price=4,quantity=4)
    r = c.place_order(config.account_id, order_limit)
    if r :
        print("=====")
        print(marketInfo[name]["symbol"]," Market Price :",marketInfo[name]["mark"])
        print("Limit Order : "+f'{name}')

    return "order filled"

# order(authenticate())
# authenticate_auto()


