from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient

import asyncio
import json
import config

client = easy_client(
        api_key=config.api_key,
        redirect_uri=config.redirect_uri,
        token_path=config.token_path)
stream_client = StreamClient(client, account_id=config.account_id)

def order_book_handler(msg):
    # print(json.dumps(msg, indent=4))
    for content in (msg["content"]):
        # print(content['BIDS'])
        for bids in content['BIDS']:
            print("EXCHANGE : ",bids["BIDS"][0]["EXCHANGE"])
            print("BID PRICE : ",bids['BID_PRICE'])
            print("VOLUME : ",bids['TOTAL_VOLUME'])
            print("-----------")


async def read_stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.DELAYED)
    await stream_client.nasdaq_book_subs(['AAPL'])

    stream_client.add_nasdaq_book_handler(order_book_handler)

    while True:
        await stream_client.handle_message()

asyncio.get_event_loop().run_until_complete(read_stream())