# Serverless tdameritrade bot

tradingview sent the alert info to AWS lambda via webhook which trigger the td ameritrade bot place the limit/market order.

### tdameritrade

tda-api : TD Ameritrade API for obtaining fundamental data, option chains, and placing orders

## Download ChromeDriver here:

https://sites.google.com/a/chromium.org/chromedriver/home
https://sites.google.com/chromium.org/driver/

### Virtual .\venv\Scripts\activate.bat

python -m venv venv
pip install virtualenv venv
.\venv\Scripts\activate.bat

### AWS CONFIGURE

pip intall boto3
pip install awscli
aws --version
aws configure
input accesskey&secret

### Chalice

chalice new-project tda
chalice deploy/local
