import logging
from datetime import datetime

import requests

from app.api.crypto_price.models import CryptoPriceResponse
from config import Config


class CryptoPriceService:

    def __init__(self):
        self.api_key = Config.COIN_MARKET_CAP_API_KEY

    def get_price(self, symbol: str) -> CryptoPriceResponse:
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": self.api_key,
        }
        logging.debug(f"Retrieving price of {symbol}")
        response = requests.get(url, headers=headers)
        if response.ok:
            quote = response.json()["data"][symbol]["quote"]["USD"]
            last_update = datetime.strptime(quote["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
            logging.info(f"Price of {symbol} is now ${quote['price']} USD")
            return CryptoPriceResponse(symbol=symbol, price=quote["price"], last_update=last_update)
        else:
            logging.error(f"Failed to retrieve price of {symbol}")
            return CryptoPriceResponse(symbol=symbol, price=0, last_update=datetime.now(), error=True)


crypto_price_service = CryptoPriceService()

if __name__ == '__main__':
    print(CryptoPriceService().get_price("DOGE"))
