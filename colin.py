import pandas as pd
from typing import List, Any, Iterable
import string
import numpy as np

class ColumnAllocator:

    CURRENCY_CODES = set("""USD EUR GBP INR AUD CAD SGD CHF MYR JPY CNY NZD THB HUF AED HKD 
                            MXN ZAR PHP SEK IDR SAR BRL TRY KES KRW EGP IQD NOK KWD RUB DKK
                            PKR ILS PLN QAR XAU OMR COP CLP TWD ARS CZK VND MAD JOD BHD XOF 
                            LKR UAH NGN TND UGX RON BDT PEN GEL XAF FJD VEF VES BYN HRK UZS
                            BGN DZD IRR DOP ISK XAG CRC SYP LYD JMD MUR GHS AOA UYU AFN LBP 
                            XPF TTD TZS ALL XCD GTQ NPR BOB ZWD BBD CUC LAK BND BWP HNL PYG
                            ETB NAD PGK SDG MOP NIO BMD KZT PAB BAM GYD YER MGA KYD MZN RSD
                            SCR AMD SBD AZN SLL TOP BZD MWK GMD BIF SOS HTG GNF MVR MNT CDF
                            STN TJS KPW MMK LSL LRD KGS GIP XPT MDL CUP KHR MKD VUV MRU ANG
                            SZL CVE SRD XPD SVC BSD XDR RWF AWG DJF BTN KMF WST SPL ERN FKP
                            SHP JEP TMT TVD IMP GGP ZMW""".split())

    # source: https://unicode.org/charts/PDF/U20A0.pdf
    CURRENCY_SYMBOLS = {"\u0024": "USD", "\u00A3": "GBP", "\u00A5": "JPY", "\u0E3F": "THB", "\u20BD": "RUB",
                        "\u20B9": "INR", "\u20AC": "EUR"}

    def __init__(self):
        pass

    def _get_stats(self, value_list: Iterable[Any]) -> float:

        all_words = ' '.join([str(v) for v in value_list])

        distinct_tokens = {w.lower() for w in all_words.split() if w.strip()}

        total_punctuations = len([t for t in all_words if t in string.punctuation])

        currency_code_ocurrences = len([w for w in all_words.split() if w.upper() in self.CURRENCY_CODES])
        currency_symbol_ocurrences = len([w for w in all_words if w in self.CURRENCY_SYMBOLS])
        word_lengths = [len(w) for w in all_words.split()]

        currency_name_score = currency_code_ocurrences + currency_symbol_ocurrences + ( 2 <= np.mean(word_lengths) <= 3)

        print('currency_name_score=', currency_name_score)
        print('total_punctuations=', total_punctuations)

    def is_currency_name(value_list: Iterable[Any]):
    
        
    
        if (
            (list_length := len(value_list)) and 
            sum(str(s).upper() in (currency.CURRENCY_CODES | currency_CURRENCY_SYMBOLS) for s in value_list) >= min(1, list_length//2)
            ):
            print('found at least ', min(1, list_length//2), ' currency CURRENCY_SYMBOLS')
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
        if (punct_CURRENCY_SYMBOLS := set(s) & set(string.punctuation)):
            puncts_per_entry += len(punct_CURRENCY_SYMBOLS)/total_entries
        if (digit_CURRENCY_SYMBOLS := set(s) & set(string.digits)):
            digits_per_entry += len(digit_CURRENCY_SYMBOLS)/total_entries

    print('average punctuation CURRENCY_SYMBOLS: ', puncts_per_entry)
    print('average digit CURRENCY_SYMBOLS: ', digits_per_entry)

    return len(distinct_tokens)/len(value_list)

if __name__ == '__main__':

    ca = ColumnAllocator()

    list_ = ["$",'AUD', 0.091, 'RUB', 'midd', None, 'dsfds', '89.95%']

    print('currency score=', ca._get_stats(list_))

    # if is_currency_name(list_):
    #     print(f'list {list_} contains currencies')
    # else:
    #     print(f'list {list_} has no currencies')

    print(is_amount(list_))

    print(is_amount([None, 1.132, 10, 35, "a"]))

    print(get_description_score(['aaa', 'aaa e12', 'aaa fqq', 'well, this is 69.95$', '12:23-1uuu']))



