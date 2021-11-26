import pandas as pd
from typing import List, Any, Iterable
from currencies import Currency
import string
import numpy as np

currency = Currency()
currency_symbols = {u.encode().decode() for u in set(currency.SYMBOLS)}

class ColumnAllocator:

    def __init__(self):
        pass

    def _get_currency_name_score(self, value_list: Iterable[Any]) -> float:

        all_words = [w.strip() for v in value_list for w in str(v).split()]

        distinct_tokens = {w.lower() for w in all_words}

        total_punctuations = sum(1 for t in all_words for ch in t if ch in string.punctuation) 

        currency_code_ocurrences = len([w for w in all_words if w.upper() in currency.CODES])
        currency_symbol_ocurrences = len([w for w in all_words if w.upper() in currency_symbols])
        word_lengths = (len(w) for w in all_words)

        currency_name_score = currency_code_ocurrences + currency_symbol_ocurrences + ( 2 <= np.mean(list(word_lengths)) <= 3)

        print('currency_name_score=', currency_name_score)
        print('total_punctuations=', total_punctuations)



    def is_currency_name(value_list: Iterable[Any]):
    
        
    
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

    ca = ColumnAllocator()

    list_ = ["$",'AUD', 0.091, 'RUB', 'midd', None, 'dsfds', '89.95%']

    print('currency score=', ca._get_currency_name_score(list_))

    # if is_currency_name(list_):
    #     print(f'list {list_} contains currencies')
    # else:
    #     print(f'list {list_} has no currencies')

    print(is_amount(list_))

    print(is_amount([None, 1.132, 10, 35, "a"]))

    print(get_description_score(['aaa', 'aaa e12', 'aaa fqq', 'well, this is 69.95$', '12:23-1uuu']))



