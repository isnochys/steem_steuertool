import django
from beem import Steem
from beem.account import Account
from beem.amount import Amount
from datetime import datetime
import requests
from dateutil import parser
import os.path
import os
from django.conf import settings
import beem
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webservice.settings")
django.setup()
from sst.models import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

media_path=os.path.join(BASE_DIR, settings.MEDIA_URL)

def get_x(cur, stamp):
	murl = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym='+cur+'&tsyms='+currency+'&ts='+str(stamp)
	f = requests.get(murl)
	d=f.json()
	print(d)
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
	
now = datetime.utcnow()

uul = Userlist.objects.filter(worker=True)
random.shuffle(uul)
for uo in uul:
	username = uo.username
	full_filename = username+'_complete.csv'
	filename=os.path.join(settings.MEDIA_URL, full_filename)

	currency = 'EUR'
	last_id =''
	if os.path.exists(filename):
		fileHandle = open(filename,"r" )
		lineList = fileHandle.readlines()
		fileHandle.close()
		if lineList:
			last_id = lineList[-1].split(';')[0]
	s = Steem()
	try:
		a = Account(username,s)
	except beem.exceptions.AccountDoesNotExistsException:
		uo.delete()
		continue
	hrl = a.history_reverse(only_ops=['producer_reward','claim_reward_balance'])
	historical_price ={}
	rtaxl = {'complete':[]}
	for op in hrl:
		if last_id == op['_id']:
			break
		timestamp = parser.parse(op['timestamp']+' UTC')
		jahr = timestamp.year
		steemx,sbdx = get_exchange_rate(timestamp)
		timestamp =timestamp.timestamp()
		if op['type']== 'claim_reward_balance':
			am = Amount(op['reward_vests']).amount
			fc = s.vests_to_sp(am,timestamp)
			euro = fc*steemx
			am = Amount(op['reward_sbd']).amount
			euro += am*sbdx
			am = Amount(op['reward_steem']).amount
			euro += am*steemx
		elif op['type']== 'producer_reward':
			am = Amount(op['vesting_shares']).amount
			fc = s.vests_to_sp(am,timestamp)
			euro = fc*steemx
		rtaxl['complete'].append({'id':op['_id'],'timestamp':op['timestamp'],'type':op['type'],'amount':euro})
		
		if jahr not in rtaxl:
			rtaxl[jahr]=[]
		rtaxl[jahr].append({'id':op['_id'],'timestamp':op['timestamp'],'type':op['type'],'amount':euro})
		
	for entr in rtaxl:
		filename = username+'_'+str(entr)+'.csv'
		filename = os.path.join(settings.MEDIA_URL, filename)
		taxl = rtaxl[entr][::-1]	
		fileHandle = open(filename,"a+")
		for tax in taxl:
			line = tax['id']+";"+tax['timestamp']+";"+tax['type']+";"+str(tax['amount'])
			fileHandle.write(line+"\n")
		fileHandle.close()
	
	uo.worker=False
	uo.save()