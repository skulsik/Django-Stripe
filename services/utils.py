import requests

from config import settings

NULLABLE = {'blank': True, 'null': True}


def currency_conversion(price_usd: float) -> int:
    """ Конверсия валюты. USD -> RUB """
    # API конвектора валюты
    api_key = settings.CURRENCY_API_KEY
    params = {'access_key': api_key, 'currencies': 'RUB', 'source': 'USD', 'format': 1}
    currency = requests.get('http://apilayer.net/api/live', params=params)
    currency = currency.json()
    price_rub: int = currency['quotes']['USDRUB']
    return price_rub


def summ_price(items: list) -> int:
    """ Суммирование всех цен """
    total_price: int = 0
    for item in items:
        price: int = item.price
        # Если валюта USD, то преобразует в рубли
        if item.currency == 'USD':
            price = price * currency_conversion(price)
        total_price += price
    return round(total_price)
