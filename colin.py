import pandas as pd
from typing import List, Any
from currencies import Currency

currency = Currency()

def is_currency(value_list: List[Any]):

    currency_symbols = {u.encode().decode() for u in set(currency.SYMBOLS)}

    if (
        (list_length := len(value_list)) and 
        sum(str(s).upper() in (currency.CODES | currency_symbols) for s in value_list) >= min(1, list_length//2)
        ):
        print('found at least ', min(1, list_length//2), ' currency symbols')
        return True
    else:
        return False

if __name__ == '__main__':

    list_ = ["$",'AUD', 0, 'RUB', 'midd', None, 'dsfds']

    if is_currency(list_):
        print(f'list {list_} contains currencies')
    else:
        print(f'list {list_} has no currencies')



