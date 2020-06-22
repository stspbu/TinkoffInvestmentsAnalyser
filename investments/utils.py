from .models import Currency


def get_currency_pair_ticker(currency_from, currency_to):
    if currency_to == Currency.RUB:
        if currency_from == Currency.USD:
            return 'USD000UTSTOM'
        elif currency_from == Currency.EUR:
            return 'EUR_RUB__TOM'

    raise NotImplementedError((currency_from, currency_to))


def get_currency_pair_figi(currency_from, currency_to):
    if currency_to == Currency.RUB:
        if currency_from == Currency.USD:
            return 'BBG0013HGFT4'
        elif currency_from == Currency.EUR:
            return 'BBG0013HJJ31'

    raise NotImplementedError((currency_from, currency_to))
