import investments


def main():
    print(f'Profit: {investments.manager.get_profit(investments.Currency.RUB)}')
    print(f'In-out-diff: {investments.manager.get_pay_in_out_diff()}')
    print(f'Dividend: {investments.manager.get_currency_to_dividend()}')
    print(f'Commission: {investments.manager.get_currency_to_commission()}')


if __name__ == '__main__':
    main()
