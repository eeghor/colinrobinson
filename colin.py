import pandas as pd
from typing import List, Any, Iterable
import string
import re
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

	def _get_stats(self, value_list: Iterable[Any], sep: str=' ') -> float:

		tokens = [w for s in value_list for w in re.split(sep, str(s))]

		print(tokens)

		floatables = re.findall(r'\d+\.\d+', ' '.join(tokens))

		print(floatables)

		punctuations = [ch for ch in ' '.join(tokens) if ch in string.punctuation]

		print(punctuations)

		currency_codes = [t for t in tokens if t.upper() in self.CURRENCY_CODES]

		print(currency_codes)

		currency_symbols = [t for t in tokens if t.upper() in self.CURRENCY_SYMBOLS]

		print(currency_symbols)

		word_lengths = [len(t) for t in tokens]

		print(word_lengths)

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



