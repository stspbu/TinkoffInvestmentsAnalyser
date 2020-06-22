from .models import Currency


def get_ticker_by_currency(currency):
    if currency == Currency.USD:
        return 'USD000UTSTOM'
    elif currency == Currency.EUR:
        return 'EUR_RUB__TOM'
    else:
        raise NotImplementedError


def get_figi_by_currency(currency):
    if currency == Currency.USD:
        return 'BBG0013HGFT4'
    elif currency == Currency.EUR:
        return 'BBG0013HJJ31'
    else:
        raise NotImplementedError(currency)
