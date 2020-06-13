import datetime


class Currency:
    RUB = 'RUB'
    USD = 'USD'


class Operation:
    class Type:
        PAY_IN = 'PayIn'
        PAY_OUT = 'PayOut'
        BUY = 'Buy'
        BUY_CARD = 'BuyCard'  # direct buy from the debit card
        SELL = 'Sell'
        DIVIDEND = 'Dividend'
        SERVICE_COMMISION = 'ServiceCommission'
        BROKER_COMMISION = 'BrokerCommission'
        MARGIN_COMMISION = 'MarginCommission'

    def __init__(self, payload):
        self.type = payload['operationType']
        self.payment = payload['payment']
        self.currency = payload['currency']
        self.dtm = _create_dtm_from_tcs_iso_dtm(payload['date'])


class Portfolio:
    def __init__(self, payload):
        self.positions = [Position(data) for data in payload['positions']]

    def get_currency_to_value(self):
        result = {}
        for p in self.positions:
            result[p.currency] = result.get(p.currency, 0) + p.value
        return result


class Position:
    def __init__(self, payload):
        self.ticker = payload['ticker']
        self.balance = payload['balance']
        self.currency = payload['averagePositionPrice']['currency']
        self.value = payload['averagePositionPrice']['value']*self.balance


class Ticker:
    class Type:
        STOCK = 'Stock'
        CURRENCY = 'Currency'

    def __init__(self, payload):
        self.figi = payload['figi']
        self.ticker = payload['ticker']
        self.type = payload['type']
        self.name = payload['name']


class Candle:
    class Interval:
        MIN1 = '1min'
        MIN2 = '2min'
        MIN3 = '3min'
        MIN5 = '5min'
        MIN10 = '10min'
        MIN15 = '15min'
        MIN30 = '30min'
        HOUR = 'hour'
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'

        @staticmethod
        def to_timedelta(interval):
            if 'min' in interval:
                val = int(interval.strip('min'))
                return datetime.timedelta(minutes=val)
            elif interval == 'hour':
                return datetime.timedelta(hours=1)
            elif interval == 'day':
                return datetime.timedelta(days=1)
            elif interval == 'week':
                return datetime.timedelta(weeks=1)
            else:
                raise NotImplementedError

    def __init__(self, payload):
        self.figi = payload['figi']
        self.interval = payload['interval']
        self.max = payload['h']
        self.min = payload['l']
        self.open = payload['o']
        self.close = payload['c']
        self.dtm = _create_dtm_from_tcs_iso_dtm(payload['time'])


def _create_dtm_from_tcs_iso_dtm(dtm_str):  # tcs jokes
    try:
        dtm = datetime.datetime.strptime(dtm_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    except:
        dtm = datetime.datetime.strptime(dtm_str, '%Y-%m-%dT%H:%M:%S%z')
    return dtm
