from .api import *
from .models import *
from . import utils

ALL = ['InvestmentsManager']


class InvestmentsManager:
    def __init__(self):
        self.api = InvestmentsAPI()

    def get_pay_in_out_diff(self, rounded=True):
        return self._calc_op_payments([Operation.Type.PAY_IN, Operation.Type.PAY_OUT], rounded=rounded)

    def get_profit(self, currency=Currency.RUB, rounded=True):
        currency_to_income = self.get_currency_to_profit(rounded=rounded)

        result = 0
        for k, v in currency_to_income.items():
            result += self._get_currency_change_cost(k, Currency.RUB) * v

        result = self._get_currency_change_cost(Currency.RUB, currency) * result
        return self._get_result(result, rounded=rounded)

    def _get_currency_change_cost(self, currency_from, currency_to):
        if currency_from == currency_to:
            return 1

        # tcs has only RUB-{CURRENCY} pairs at the moment
        if currency_from == Currency.RUB:
            figi = utils.get_currency_pair_figi(currency_to, currency_from)
            last_candle = self.api.get_candles(figi, Candle.Interval.WEEK)[0]
            change_cost = 1 / last_candle.close
        else:
            figi = utils.get_currency_pair_figi(currency_from, currency_to)
            last_candle = self.api.get_candles(figi, Candle.Interval.WEEK)[0]
            change_cost = last_candle.close

        return change_cost

    def get_currency_to_profit(self, rounded=True):
        portfolio = self.api.get_portfolio()
        portfolio_data = portfolio.get_currency_to_value()
        payments_data = self._calc_op_payments([Operation.Type.PAY_IN, Operation.Type.PAY_OUT], rounded=rounded)
        payments_data = {k: -1*v for k, v in payments_data.items()}

        result = {}
        for k, v in list(portfolio_data.items()) + list(payments_data.items()):
            result[k] = result.get(k, 0) + v
        return self._get_result(result, rounded=rounded)

    def get_currency_to_dividend(self, rounded=True):
        return self._calc_op_payments([Operation.Type.DIVIDEND], rounded=rounded)

    def get_currency_to_commission(self, rounded=True):
        return self._calc_op_payments([
            Operation.Type.BROKER_COMMISION,
            Operation.Type.SERVICE_COMMISION,
            Operation.Type.MARGIN_COMMISION], rounded=rounded)

    def _calc_op_payments(self, op_types, rounded=True):
        type_to_ops = self.get_type_to_operations()

        result = {}
        for op_type in op_types:
            for op in type_to_ops[op_type]:
                result[op.currency] = result.get(op.currency, 0) + op.payment
        return self._get_result(result, rounded=rounded)

    @staticmethod
    def _get_result(result, rounded=True):
        if rounded:
            if isinstance(result, dict):
                result = {k: round(v, 3) for k, v in result.items()}
            elif isinstance(result, float):
                result = round(result, 3)
        return result

    def get_type_to_operations(self, dtm_from=None, dtm_to=None, currency=None):
        operations = self.api.get_operations(dtm_from=dtm_from, dtm_to=dtm_to)

        result = {}
        for op in operations:
            if currency and op.currency != currency:
                continue

            lst = result.setdefault(op.type, [])
            lst.append(op)
        return result

