from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Userlist
from datetime import datetime,timedelta
from dateutil import parser
from django.conf import settings
import os

def index(request):
	context = {}
	context['created']=False
	if request.method == 'POST':
		if 'inputUsername' in request.POST:
			username = request.POST['inputUsername']
			context['username']=username
			mdc,cre = Userlist.objects.get_or_create(username=username)
			woc = Userlist.objects.filter(worker=True).count()
			context['woc'] = woc
			context['dauer'] = woc*15
			if cre:
				context['created'] = True
			else:
				if mdc.worker == True:
					context['worker']=True
				else:
					context['out']=mdc
					now = datetime.utcnow()
					if parser.parse(str(now)+' UTC') - mdc.dateAdded > timedelta(days=2):
						mdc.worker=True
						mdc.save()
						context['worker']=True
					else:
						pth = settings.MEDIA_ROOT
						files = [i for i in os.listdir(pth) if os.path.isfile(os.path.join(pth,i)) and username+'_' in i]
						context['files']=files
	return render(request, 'sst/index.html', context)