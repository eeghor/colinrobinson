import pandas as pd
from typing import List, Any
from currencies import Currency
import string

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

def is_amount(value_list: List[Any]):

    total_floatable = 0
    decimals = []

    for s in value_list:
        for w in str(s).split():
            try:
                total_floatable += (float(w) >= 0)
                if '.' in w:
                    decimals.append(len(w.split('.')[-1]))
            except:
                pass

    print('average decimals: ', sum(decimals)/len(value_list))
    if total_floatable >= max(1, len(value_list)//2):
        print(f'floatables: {total_floatable}/{len(value_list)}')
        return True
    else:
        return False

def get_description_score(value_list: List[Any]):

    distinct_tokens = set()
    puncts_per_entry = 0
    digits_per_entry = 0

    total_entries = len(value_list)

    for s in value_list:
        distinct_tokens |= set(str(s).lower().split())
        if (punct_symbols := set(s) & set(string.punctuation)):
            puncts_per_entry += len(punct_symbols)/total_entries
        if (digit_symbols := set(s) & set(string.digits)):
            digits_per_entry += len(digit_symbols)/total_entries

    print('average punctuation symbols: ', puncts_per_entry)
    print('average digit symbols: ', digits_per_entry)

    return len(distinct_tokens)/len(value_list)

if __name__ == '__main__':

    list_ = ["$",'AUD', 0.091, 'RUB', 'midd', None, 'dsfds', '89.95%']

    if is_currency(list_):
        print(f'list {list_} contains currencies')
    else:
        print(f'list {list_} has no currencies')

    print(is_amount(list_))

    print(is_amount([None, 1.132, 10, 35, "a"]))

    print(get_description_score(['aaa', 'aaa e12', 'aaa fqq', 'well, this is 69.95$', '12:23-1uuu']))



