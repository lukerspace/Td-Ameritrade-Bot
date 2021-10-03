# Serverless tdameritrade bot

tdameritrade bot get the signal from AWS Lambda using Python Chalice library and the signal came from webhook url from tradingview alert.

# tdameritrade

TD Ameritrade API examples for obtaining fundamental data, option chains, and placing orders

## Download ChromeDriver here:

https://sites.google.com/a/chromium.org/chromedriver/home

### Virtual .\venv\Scripts\activate.bat

pip install virtualenv venv
.\venv\Scripts\activate.bat

### AWS CONFIGURE

pip intall boto3
pip install awscli
aws --version
aws accesskey&secret
chalice new-project tradingview
chalice deploy/local
