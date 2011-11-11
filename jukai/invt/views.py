from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from jukai.invt.models import Part, PartForm
from django.http import HttpResponse

def index(request):
	latest_part = Part.objects.all().order_by('id')[:1000]
	return render_to_response('html/hoge.html',
		{'latest_part': latest_part},
		context_instance=RequestContext(request))

def update(request,length=10000):
	latest_part = Part.objects.all().order_by('-up_date')[:length]
	return render_to_response('html/hoge.html',
		{'latest_part': latest_part,
		'update': True,
		'length': length},
		context_instance=RequestContext(request)
		)

def popular(request,length=10000):
	latest_part = Part.objects.all().order_by('-Hnum')[:length]
	return render_to_response('html/hoge.html',
		{'latest_part': latest_part,
		'popular': True,
		'length': length},
		context_instance=RequestContext(request)
		)

def editor(request,part_id):
	if request.user.is_authenticated():
		partobj = Part.objects.get(id=part_id)
		if request.method == 'POST':
			partobj.up_date=datetime.datetime.now()
			update_partobj = PartForm(request.POST,instance=partobj)
			if update_partobj.is_valid():
				update_partobj.save()
				return HttpResponseRedirect('/jukai')
			else:
				return HttpResponseRedirect('/Oops')
		else:
			form = PartForm(instance=partobj)
		return render_to_response('html/om.html',
			{'form' : form},
			context_instance=RequestContext(request)
			)
	else:
		return HttpResponseRedirect('/login')

def partadd(request):
	if request.user.is_authenticated():
		partobj = Part()
		partobj.pub_date = datetime.datetime.now()
		partobj.up_date = datetime.datetime.now()
		if request.method == 'POST':
			new_part = PartForm(request.POST,instance=partobj)
			if new_part.is_valid():
				new_part.save()
				return HttpResponseRedirect('/jukai')
			else:
				return HttpResponseRedirect('/Oops')
		else:
			form = PartForm()
		return render_to_response('html/om.html',
			{'form' : form},
			context_instance=RequestContext(request)
			)
	else:
		return HttpResponseRedirect('/login')


