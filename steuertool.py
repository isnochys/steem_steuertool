from steem import Steem
from steem.account import Account
from steem.amount import Amount
from steem.converter import Converter
from datetime import datetime
import requests
from dateutil import parser
import os.path

username = 'isnochys'
filename = 'steuer.csv'
currency = 'EUR'

last_id =''
if os.path.exists(filename):
	fileHandle = open(filename,"r" )
	lineList = fileHandle.readlines()
	fileHandle.close()
	if lineList:
		last_id = lineList[-1].split(';')[0]
	
s = Steem()
a = Account(username,s)
con = Converter(s)
hrl = a.history_reverse(filter_by=['producer_reward','claim_reward_balance'])
historical_price ={}
rtaxl = []
vests_steem = con.vests_to_sp(1)

def get_x(cur, stamp):
	#'https://min-api.cryptocompare.com/data/pricehistorical?fsym=STEEM&tsyms=BTC,USD,EUR&ts=1502689400'
	murl = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym='+cur+'&tsyms='+currency+'&ts='+str(stamp)
	f = requests.get(murl)
	d=f.json()
	return d[cur][currency]#rate
	
def get_exchange_rate(timestamp):
	datum = str(timestamp.year)+"-"+str(timestamp.month)+"-"+str(timestamp.day)
	if datum not in historical_price:
		tmpstp = parser.parse(datum+' 00:00:00 UTC').timestamp()
		steemx = get_x('STEEM',tmpstp)
		sbdx = get_x('SBD',tmpstp)
		historical_price[datum]={'STEEM':steemx,'SBD':sbdx}
	ret = historical_price[datum]
	return ret['STEEM'],ret['SBD']
	
for op in hrl:
	if last_id == op['_id']:
		break
	timestamp = parser.parse(op['timestamp']+' UTC')
	steemx,sbdx = get_exchange_rate(timestamp)
	if op['type']== 'claim_reward_balance':
		am = Amount(op['reward_vests']).amount
		euro = am*vests_steem*steemx
		am = Amount(op['reward_sbd']).amount
		euro += am*sbdx
		am = Amount(op['reward_steem']).amount
		euro += am*steemx
	elif op['type']== 'producer_reward':
		am = Amount(op['vesting_shares']).amount
		euro = am*vests_steem*steemx
	rtaxl.append({'id':op['_id'],'timestamp':op['timestamp'],'type':op['type'],'amount':euro})

taxl = rtaxl[::-1]	
fileHandle = open(filename,"a")
for tax in taxl:
	line = tax['id']+";"+tax['timestamp']+";"+tax['type']+";"+str(tax['amount'])
	fileHandle.write(line+"\n")
fileHandle.close()