from dataclasses import dataclass
from datetime import datetime


@dataclass
class CryptoPriceResponse:
    symbol: str
    price: float
    last_update: datetime
    currency: str = "USD"
    error: bool = False
