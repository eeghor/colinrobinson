import pandas as pd
from collections import defaultdict
from typing import List, Any, Iterable
import string
import re
import numpy as np

class ColumnAllocator:

	"""
	This class looks at the columns of a supplied data frame and decides which of them
	should be 

	 - amout
	 - currency
	 - description
	 - coding
	"""

	def _tokenized(self, value_list: Iterable[Any], sep: str=' ') -> str:
		for s in value_list:
			for w in re.split(sep, str(s)):
				yield w.strip()


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
	CURRENCY_SYMBOLS = {k.encode().decode(): v for k, v in {"\u0024": "USD", "\u00A3": "GBP", "\u00A5": "JPY", "\u0E3F": "THB", "\u20BD": "RUB",
															"\u20B9": "INR", "\u20AC": "EUR"}.items()}

	CURRENCY_CODE_LENGTHS = {2,3}

	def score_input(self, value_list: Iterable[Any]) -> float:

		average_per_row = defaultdict(float)

		total_values = len(value_list)

		for token in self._tokenized(value_list):

			average_per_row['floatables'] += len(re.findall(r'\d+\.\d+', token))/total_values
			average_per_row['punctuations'] += sum(ch in string.punctuation for ch in token)/total_values
			average_per_row['currency_codes'] += (token.upper() in self.CURRENCY_CODES)/total_values
			average_per_row['currency_symbols'] += (token in self.CURRENCY_SYMBOLS)/total_values
			average_per_row['word_lengths'] += len(token)/total_values
			average_per_row['uppers'] += token.isupper()/total_values

		scores = defaultdict(float)

		scores['currency_name'] = (average_per_row['word_lengths'] in self.CURRENCY_CODE_LENGTHS) + \
								  (average_per_row['currency_codes'] >= 0.50) + \
								  (average_per_row['uppers'] > 0) + \
								  (average_per_row['currency_symbols'] > 0.10)  - \
								  (average_per_row['floatables'] > 0) - \
								  (average_per_row['punctuations'] > 0)   

		scores['amount'] = (average_per_row['word_lengths'] >= 3) - \
						   (average_per_row['currency_codes'] >= 0) -\
						   (average_per_row['uppers'] > 0) + \
						   (average_per_row['currency_symbols'] > 0)  + \
						   (average_per_row['floatables'] > 0.50) 

		scores['description'] = (average_per_row['word_lengths'] > 3) - \
								(average_per_row['currency_codes'] >= 0.10) - \
								(average_per_row['currency_symbols'] > 0.10)  - \
								(average_per_row['floatables'] > 0.20) + \
								(average_per_row['punctuations'] > 0.10) 

		return scores

	def allocate_columns(self, data: pd.DataFrame = None):

		scores_by_column = defaultdict(lambda: defaultdict(float))

		for c in data.columns:

			scores_by_column[c] = self.score_input(data[c])


		print(scores_by_column)

		collumn_allocation = defaultdict(str)

		for _ in 'amount currency_name description'.split():
			collumn_allocation[_] = max(scores_by_column, key = lambda k: scores_by_column[k][_])

		print(collumn_allocation)

if __name__ == '__main__':

	ca = ColumnAllocator()

	df = pd.DataFrame({'dollars': [23.8, 1.950, 19.90, None],
				  'crc': ['INR', '$', 'UAH', 'JPY'],
				  'desc': 'this stгаа шы someting -2323куфддн ащк Ьшлуб 12/2020'})

	ca.allocate_columns(df)