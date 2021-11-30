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

	def score_input(self, value_list: Iterable[Any], sep: str=' ') -> float:

		tokens = [w.strip() for s in value_list for w in re.split(sep, str(s))]

		floatables = re.findall(r'\d+\.\d+', ' '.join(tokens))

		punctuations = [ch for ch in ' '.join(tokens) if ch in string.punctuation]

		currency_codes = [t for t in tokens if t.upper() in self.CURRENCY_CODES]

		currency_symbols = [t for t in tokens if t in self.CURRENCY_SYMBOLS]

		word_lengths = [len(t) for t in tokens]

		score = {'currency_name': len(currency_codes) + len(set(currency_symbols)) + sum([2 <= l <= 3 for l in word_lengths]),
				 'amount': len(floatables) + len(set(currency_symbols)), 
				 'description': len(punctuations) + np.mean(word_lengths)}

		return score

	def allocate_columns(self, data: pd.DataFrame = None):

		for c in data.columns:

			scores = self.score_input(data[c])




if __name__ == '__main__':

	ca = ColumnAllocator()

	list_ = ["$",'AUD', 0.091, 'RUB', 'midd', None, 'dsfds', '89.95%', 3]

	print('currency score=', ca.score_input(list_))