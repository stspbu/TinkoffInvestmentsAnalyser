from .models import Currency


def get_ticker_by_currency(currency):
    if currency == Currency.USD:
        return 'USD000UTSTOM'
    else:
        raise NotImplementedError


def get_figi_by_currency(currency):
    if currency == Currency.USD:
        return 'BBG0013HGFT4'
    else:
        raise NotImplementedError(currency)
