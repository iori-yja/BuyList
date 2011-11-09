from django.shortcuts import render_to_response
import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from jukai.invt.models import Part, PartForm
from django.http import HttpResponse

def index(request):
	latest_part = Part.objects.all().order_by('id')[:5]
	return render_to_response('html/hoge.html',
		{'latest_part': latest_part})

def update(request,length=10000):
	latest_part = Part.objects.all().order_by('up_date')[:length]
	return render_to_response('html/hoge.html',
		{'latest_part': latest_part,
		'update': True,
		'length': length}
		)

def popular(request,length=10000):
	latest_part = Part.objects.all().order_by('Hnum')[:length]
	return render_to_response('html/hoge.html',
		{'latest_part': latest_part,
		'popular': True,
		'length': length}
		)

def editor(request,part_id):
	if request.method == 'POST':
		form = PartForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/hoge/')
	else:
		partobj = Part.objects.get(id=part_id)
		form = PartForm(instance=partobj)
	return render_to_response('html/om.html',
		{'form' : form}
		)

def form(request):
	if request.method == 'POST':
		form = PartForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = PartForm()
	return render_to_response('html/om.html',
		{'form' : form}
		)

