import requests
import datetime
import logging

import settings
from .models import Operation, Portfolio, Candle, Ticker

ALL = ['InvestmentsAPI']


class InvestmentsAPI:
    API_URL = 'https://api-invest.tinkoff.ru/openapi'
    SANDBOX_URL = 'https://api-invest.tinkoff.ru/openapi/sandbox'

    def get_candles(self, figi, interval, dtm_from=None, dtm_to=None):
        if not dtm_from:
            dtm_from = datetime.datetime.now(tz=datetime.timezone.utc) - Candle.Interval.to_timedelta(interval)

        if not dtm_to:
            dtm_to = datetime.datetime.now(tz=datetime.timezone.utc)

        r = self._make_request('/market/candles', params={
            'from': dtm_from.isoformat(),
            'to': dtm_to.isoformat(),
            'figi': figi,
            'interval': interval
        })
        return [Candle(data) for data in r['payload']['candles']]

    def get_portfolio(self):
        r = self._make_request('/portfolio')
        return Portfolio(r['payload'])

    def get_operations(self, dtm_from=None, dtm_to=None):
        if not dtm_from:
            dtm_from = datetime.datetime(year=1998, month=7, day=2, tzinfo=datetime.timezone.utc)

        if not dtm_to:
            dtm_to = datetime.datetime.now(tz=datetime.timezone.utc)

        r = self._make_request('/operations', params={'from': dtm_from.isoformat(), 'to': dtm_to.isoformat()})
        return [Operation(data) for data in r['payload']['operations']]

    def get_ticker(self, ticker):
        r = self._make_request('/market/search/by-ticker', params={'ticker': ticker})
        return Ticker(r['payload']['instruments'][0])

    def _make_request(self, endpoint, params=None, test_mode=False):
        if not test_mode:
            base_url = self.API_URL
            token = settings.get("api_token")
        else:
            base_url = self.SANDBOX_URL
            token = settings.get("sandbox_token")

        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(f'{base_url}{endpoint}', headers=headers, params=params)

        if response.status_code != 200:
            logging.warning(f'Failed to make a request; status={response.status_code}, content={response.content}')
            raise APIException()

        try:
            response_data = response.json()
        except:
            logging.warning(f'Failed to deserialize response data; content={response.content}')
            raise

        return response_data


class APIException(Exception):
    pass
