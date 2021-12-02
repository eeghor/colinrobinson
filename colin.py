import pandas as pd
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

	def score_input(self, value_list: Iterable[Any]) -> float:

		floatables = punctuations = currency_codes = 0
		currency_symbols = word_lengths = 0

		total_values = len(value_list)

		for token in self._tokenized(value_list):

			floatables += len(re.findall(r'\d+\.\d+', token))
			punctuations += sum(ch in string.punctuation for ch in token)
			currency_codes += (token.upper() in self.CURRENCY_CODES)
			currency_symbols += (token in self.CURRENCY_SYMBOLS)
			word_lengths += len(token)

		is_amount = True if floatables/total_values >= 0.5 else False

		print(f"floatables={floatables}, punctuations={punctuations}, currency_codes={currency_codes}, currency_symbols={currency_symbols}, word_lengths={word_lengths}")

	def allocate_columns(self, data: pd.DataFrame = None):

		for c in data.columns:

			scores = self.score_input(data[c])




if __name__ == '__main__':

	ca = ColumnAllocator()

	list_ = ["$",'AUD', 0.091, 'RUB', 'midd', None, 'dsfds', '89.95%', 3, "\u20B9".encode().decode()]

	ca.score_input(list_)