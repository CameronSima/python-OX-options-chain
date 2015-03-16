import urllib2
from bs4 import BeautifulSoup


"""
USAGE:

option = OptionChain('SPY')

option.all 					 returns a nested dictionary returning all option data.
option.calls 				 returns a nested dictionary containing all calls data.
option.puts 				 returns a nested dictionary containing all puts data.

chain.calls['itm']			 returns a list of dictionaries containing in-the-money 
							 calls elements.

for x in chain.calls['itm']:
	x['theo']  				 returns theoretical values for every itm call option.
	

"""

URL = ('https://www.optionsxpress.com.au/'
	   'OXNetTools/Chains/index.aspx?Chai'
	   'nType=3&SessionID=C73763A1C9E747C'
	   'DBDB18D0276D6B780')

def payload(symbol, call_put):
	"""callput == 'C' or 'P'"""
	data = '{"args":{"symbol":"%s",:"91","callput":"%s","sessionid":"C73763A1C9E747CDBDB18D0276D6B78"}}' % (symbol, call_put)
	return data

def rows(response):
	soup = BeautifulSoup(response)
	return soup('tr', {'onmouseout': 'KillTimer();'})

def otm(results):
	otms = [(x, 'otm') for x in results if x.find(class_='otm')]
	return otms

def itm(results):
	itms = [(x, 'itm') for x in results if x.find(class_='itm')]
	return itms

def get_element(row, element_no):
	element = row.text.splitlines()[element_no]
	return float(element)


def get_dict(row):
	element_dict = {
		'strike': get_element(row[0], 1),
		'last' : get_element(row[0], 2),
		'bid' : get_element(row[0], 3),
		'ask' : get_element(row[0], 4),
		'theo' : get_element(row[0], 5),
		'itm_or_otm' : row[1],
		}

	return element_dict

def dict_list(rows):
	return [get_dict(x) for x in rows]

class OptionChain():
	def __init__(self, symbol):
		"""
		Usage:

		chain=OptionChain('SPY')

		chain.all
		chain.puts
		chain.calls

		option = chain.calls[0]

		"""


		opener = urllib2.build_opener()
		opener.addheaders.append(('Cookie', 
			'OXAUTH=005C769B847B6B465E95C80FF3019F5C86;'
			' ASP.NET_SessionId=zrkbp2zvdjmjk0yqhu1zhaz'
			't; OXDOMAIN=.optionsxpress.com.au; TLTSID='
			'6C1A137140F7601584B71BBD88778CEB; Firm=OB'))

		call_payload = payload(symbol, 'C')
		put_payload = payload(symbol, 'P')

		calls_request = opener.open(URL, data=call_payload)
		puts_request = opener.open(URL, data=put_payload)

		calls = calls_request.read()
		puts = puts_request.read()

		itm_calls = dict_list(itm(rows(calls)))
		itm_puts = dict_list(itm(rows(puts)))
		otm_calls = dict_list(otm(rows(calls)))
		otm_puts = dict_list(otm(rows(puts)))

		root = {'chain': {'calls': {'itm': [], 'otm': []}, 'puts': {'itm': [], 'otm': []}}}
		
		for x in itm_calls:
			root['chain']['calls']['itm'].append(x)

		for x in otm_calls:
			root['chain']['calls']['otm'].append(x)

		for x in itm_puts:
			root['chain']['puts']['itm'].append(x)

		for x in otm_puts:
			root['chain']['puts']['otm'].append(x)


		self.all = root
		self.calls = root['chain']['calls']
		self.puts = root['chain']['puts']



