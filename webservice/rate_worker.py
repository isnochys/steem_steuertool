import django
from beem import Steem
from beem.account import Account
from beem.amount import Amount
from datetime import datetime, timedelta
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
currency = 'EUR'
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
	
timestamp = datetime.utcnow()
steemcre = True
sbdcre = True
while steemcre or sbdcre:
	datum = str(timestamp.year)+"-"+str(timestamp.month)+"-"+str(timestamp.day)
	steemdb, steemcre = Rates.objects.get_or_create(datum=datum,currency='STEEM')
	sbddb, sbdcre = Rates.objects.get_or_create(datum=datum,currency='SBD')
	if steemcre or sbdcre:
		tmpstp = parser.parse(datum+' 00:00:00 UTC').timestamp()
		steemx = get_x('STEEM',tmpstp)
		sbdx = get_x('SBD',tmpstp)
		steemdb.rate = steemx
		sbddb.rate = sbdx
		steemdb.save()
		sbddb.save()
	timestamp -= timedelta(days=1)	
		
	