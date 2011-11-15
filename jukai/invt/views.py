from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from jukai.invt.models import *
from django.http import HttpResponse

def index(request):
	latest_part_list = Part.objects.all().order_by('id')[:1000]
	nee = [ Parter(latest_part) for latest_part in latest_part_list ]
	return render_to_response('html/hoge.html',
		{'needs': nee},
		context_instance=RequestContext(request))

class Parter:
	def __init__(self, latest_part):
		self.latest_part = latest_part
		all_req = self.latest_part.req_set.all()[:10]
		self.up_date = 0
		if all_req:	self.up_date = all_req[0].up_date
		else:		self.up_date = 'Not yet'
		if self.latest_part.req_set.all()[:10]:
			self.allneeds   = reduce( lambda x,y:x+y, [ req.allneeds for req in all_req ] )
			self.Mlevneeds = reduce( lambda x,y:x+y, [ req.Mnum for req in all_req ] )
			self.Alevneeds  = reduce( lambda x,y:x+y, [ req.Anum for req in all_req ] )
			self.Blevneeds  = reduce( lambda x,y:x+y, [ req.Bnum for req in all_req ] )
			self.Clevneeds  = reduce( lambda x,y:x+y, [ req.Cnum for req in all_req ] )
		else:
			self.allneeds  = 1000
			self.Mlevneeds = 0
			self.Alevneeds = 0
			self.Blevneeds = 0
			self.Clevneeds = 0

class Nudes:
	def __init__(self, latest_req):
		self.latest_part = latest_req.partype
		self.up_date = latest_req.up_date
		all_req = self.latest_part.req_set.all()
		self.allneeds   = reduce( lambda x,y:x+y, [ req.allneeds for req in all_req ] )
		self.Mlevneeds = reduce( lambda x,y:x+y, [ req.Mnum for req in all_req ] )
		self.Alevneeds  = reduce( lambda x,y:x+y, [ req.Anum for req in all_req ] )
		self.Blevneeds  = reduce( lambda x,y:x+y, [ req.Bnum for req in all_req ] )
		self.Clevneeds  = reduce( lambda x,y:x+y, [ req.Cnum for req in all_req ] )

def update(request,length=10000):
	latest_req_list = Req.objects.all().order_by('-up_date')[:length]
	nee = [ Nudes(latest_req) for latest_req in latest_req_list ]
	return render_to_response('html/hoge.html',
		{'needs': nee,
		'update': True,
		'length': length},
		context_instance=RequestContext(request)
		)

#def popular(request,length=10000):
#	latest_part = Part.objects.all().order_by('-Hnum')[:length]
#	return render_to_response('html/hoge.html',
#		{'latest_part': latest_part,
#		'popular': True,
#		'length': length},
#		context_instance=RequestContext(request)
#		)
#
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

def request(request,part_id):
	if request.user.is_authenticated():
		reqobj = Req()
		reqobj.partype = Part.objects.get(id=part_id)
		reqobj.pub_date = datetime.datetime.now()
		reqobj.up_date = datetime.datetime.now()
		if request.method == 'POST':
			req = PartForm(request.POST,instance=reqobj)
			if req.is_valid():
				req.save()
				return HttpResponseRedirect('/jukai')
			else:
				return HttpResponseRedirect('/Oops')
		else:
			form = ReqForm(instance=reqobj)
		return render_to_response('html/om.html',
			{'form' : form},
			context_instance=RequestContext(request)
			)
	else:
		return HttpResponseRedirect('/login')

#def delete(request, part_id):
#	if request.user.is_authenticated():
#		partobj = Part.objects.get(id=part_id)
#		partobj.delete()
#		return HttpResponseRedirect('/jukai')
#	else:
#		return HttpResponseRedirect('/Oops')
#
