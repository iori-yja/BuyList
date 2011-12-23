import datetime
import operator
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from jukai.invt.models import *
from django.http import HttpResponse


class Parter:
	def __init__(self, latest_part):
		self.latest_part = latest_part
		self.all_req = self.latest_part.req_set.all()
		all_req = self.all_req
		self.up_date = 0
		self.prop = mkprop(latest_part)
		if all_req:	self.up_date = all_req[0].up_date
		else:		self.up_date = 'Not yet'
		if self.latest_part.req_set.all():
			self.allneeds   = reduce( lambda x,y:x+y, [ req.allneeds() for req in all_req ] )
			self.Mlevneeds = reduce( lambda x,y:x+y, [ req.Mnum for req in all_req ] )
			self.Alevneeds  = reduce( lambda x,y:x+y, [ req.Anum for req in all_req ] )
			self.Blevneeds  = reduce( lambda x,y:x+y, [ req.Bnum for req in all_req ] )
			self.Clevneeds  = reduce( lambda x,y:x+y, [ req.Cnum for req in all_req ] )
		else:
			self.allneeds  = 0
			self.Mlevneeds = 0
			self.Alevneeds = 0
			self.Blevneeds = 0
			self.Clevneeds = 0


class Needs:
	def __init__(self, latest_req):
		self.latest_part = latest_req.partype
		self.prop = mkprop(latest_req.partype)
		self.up_date = latest_req.up_date
		all_req = self.latest_part.req_set.all()
		self.allneeds   = reduce( lambda x,y:x+y, [ req.allneeds() for req in all_req ] )
		self.Mlevneeds = reduce( lambda x,y:x+y, [ req.Mnum for req in all_req ] )
		self.Alevneeds  = reduce( lambda x,y:x+y, [ req.Anum for req in all_req ] )
		self.Blevneeds  = reduce( lambda x,y:x+y, [ req.Bnum for req in all_req ] )
		self.Clevneeds  = reduce( lambda x,y:x+y, [ req.Cnum for req in all_req ] )

class Reqlist:
	def __init__(self, latest_req):
		self.latest_part = latest_req.partype
		self.prop = mkprop(self.latest_part)
		self.up_date = latest_req.up_date
		self.allneeds   = latest_req.allneeds   
		self.Mlevneeds  = latest_req.Mnum  
		self.Alevneeds  = latest_req.Anum  
		self.Blevneeds  = latest_req.Bnum  
		self.Clevneeds  = latest_req.Cnum  

def deletenullreqdb():
	latest_req_list = Req.objects.all()
	reduce((lambda x, y: y.allneeds() == 0 and y.delete() or 0), latest_req_list, 1)

def reportbought(part_id, num):
	def deleterequestM(partreq,num):
		pl = partreq
		while pl != [] and num > 0:
			if pl[0].Mnum > num:
				pl[0].Mnum = partreq.Mnum - num
			else:
				num = num - pl[0].Mnum
				pl[0].Mnum = 0
			pl[0].save()
			pl = pl[1:]
		return num
	def deleterequestA(partreq,num):
		pl = partreq
		while pl != [] and num > 0:
			if pl[0].Anum > num:
				pl[0].Anum = partreq.Anum - num
			else:
				num = num - pl[0].Anum
				pl[0].Anum = 0
			pl[0].save()
			pl = pl[1:]
		return num
	def deleterequestB(partreq,num):
		pl = partreq
		while pl != [] and num > 0:
			if pl[0].Bnum > num:
				pl[0].Bnum = partreq.Bnum - num
			else:
				num = num - pl[0].Bnum
				pl[0].Bnum = 0
			pl[0].save()
			pl = pl[1:]
		return num
	def deleterequestC(partreq,num):
		pl = partreq
		while pl != [] and num > 0:
			if pl[0].Cnum > num:
				pl[0].Cnum = partreq.Cnum - num
			else:
				num = num - pl[0].Cnum
				pl[0].Cnum = 0
			pl[0].save()
			pl = pl[1:]
		return num
	partobj = Part.objects.get(id=part_id)
	partreq = Parter(partobj).all_req
	if num > 0: num = deleterequestM(partreq,num)
	if num > 0: num = deleterequestA(partreq,num)
	if num > 0: num = deleterequestB(partreq,num)
	if num > 0: num = deleterequestC(partreq,num)
	deletenullreqdb()
	return num

def listreqs(request):
	latest_req_list = Req.objects.all().order_by('-up_date')
	nee = [ Reqlist(latest_req) for latest_req in latest_req_list ]
	return render_to_response('html/hoge.html',
		{'needs': nee,
		 'reqs': True},
		context_instance=RequestContext(request))

def index(request):
	latest_part_list = Part.objects.all().order_by('id')[:1000]
	nee = [ Parter(latest_part) for latest_part in latest_part_list ]
	return render_to_response('html/hoge.html',
		{'needs': nee},
		context_instance=RequestContext(request))


def new(request,length=10000):
	latest_req_list = Req.objects.all().order_by('-up_date')[:length]
	nee = [ Needs(latest_req) for latest_req in latest_req_list ]
	nee = reduce( lambda xs,y: xs if filter(lambda x:x.latest_part==y.latest_part,xs) else xs+[y], nee, [])
	return render_to_response('html/hoge.html',
		{'needs': nee,
		'update': True,
		'length': length},
		context_instance=RequestContext(request)
		)

def resistored(request,length=10000):
	return render_to_response('html/resistored.html',
		{},
		context_instance=RequestContext(request)
		)
def popular(request,length=10000):
	latest_part_list = Part.objects.all().order_by('id')[:length]
	nee = [ Parter(latest_part) for latest_part in latest_part_list ]
	new = sorted(nee,reverse=True,key=operator.attrgetter('allneeds'))
	return render_to_response('html/hoge.html',
		{'needs': new,
		'popular': True,
		'length': length},
		context_instance=RequestContext(request)
		)
def editor(request,part_id):
	if request.user.is_authenticated():
		partobj = Part.objects.get(id=part_id)
		if request.method == 'POST':
			update_partobj = PartForm(request.POST,instance=partobj)
			if update_partobj.is_valid():
				update_partobj.save()
				return HttpResponseRedirect('/jukai')
			else:
				return render_to_response('html/om.html',
					{'bug': update_partobj,
					'debug' : True},
					context_instance=RequestContext(request))
		else:
			form = PartForm(instance=partobj)
		return render_to_response('html/om.html',
			{'form' : form,},
			context_instance=RequestContext(request)
			)
	else:
		return HttpResponseRedirect('/login')

def partadd(request,sp='none'):
	"""
	This method is called when user pull a form to create new part, and to post it.
	User must be authenticated.
	"""
	if request.user.is_authenticated():
		if request.method == 'POST':
			partobj = newobj(sp)
			partobj.user = request.user
			new_part = getformwitharg(sp,request.POST,instance=partobj)
			if new_part.is_valid():
				new_part.save()
				return HttpResponseRedirect('/registered')
			else:
				return HttpResponseRedirect('/Oops')
		else: #GET Method
			if sp == 'none':
				return render_to_response('html/addchoice.html',
					context_instance=RequestContext(request)
					)
			else:
				form = getform(sp)
				return render_to_response('html/om.html',
					{'form' : form,
					 'decent':sp},
					context_instance=RequestContext(request)
					)
	else:
		return HttpResponseRedirect('/login')

def request(request,part_id):
	if request.user.is_authenticated():
		reqobj = Req()
		reqobj.partype = Part.objects.get(id=part_id)
		reqobj.user = request.user
		if request.method == 'POST':
			update_req = ReqForm(request.POST,instance=reqobj)
			if update_req.is_valid():
				update_req.save()
				return HttpResponseRedirect('/resistored')
			else:
				form=update_req.errors
		else:
			form = ReqForm(instance=reqobj)
		return render_to_response('html/fuga.html',
			{'form' : form},
			context_instance=RequestContext(request)
			)
	else:
		return HttpResponseRedirect('/login')

def deleterequest(request,req_id):
	if request.user.is_authenticated():
		reqobj = Reqs.objects.get(id=req_id)
		reqobj.delete()
		return HttpResponseRedirect('/jukai')
	else:
		return HttpResponseRedirect('/Oops')

def deletepart(request,part_id):
	if request.user.is_authenticated():
		partobj = Part.objects.get(id=part_id)
		objdelete(partobj)
		return HttpResponseRedirect('/jukai')
	else:
		return HttpResponseRedirect('/Oops')


def webreport(request):
	if request.user.is_authenticated():
		if request.method == 'GET':
			latest_part_list = Part.objects.all().order_by('id')
			nee = [ Parter(latest_part) for latest_part in latest_part_list ]
			new = sorted(nee,reverse=True,key=operator.attrgetter('allneeds'))
			return render_to_response('html/hoge.html',
				{"needs":new,
				"report":True},
				context_instance=RequestContext(request))
		else:
			maper(request.POST)
			return HttpResponseRedirect('/Thanks!')
	else: HttpResponseRedirect('/login')

def user(request,user_id='none'):
	if user_id=='none':
		if request.user.is_authenticated():
			return HttpResponseRedirect(('/jukai/user/'+str(request.user.id)))
		else:
			return HttpResponseRedirect('/login')
	else:
		if request.user.is_authenticated():
			parts = filter(lambda x:str(x.user.id)==user_id,Part.objects.all())
			parts = [ Parter(part) for part in parts ]
			requests = filter(lambda x:str(x.user.id)==user_id,Req.objects.all())
			requests = [ Reqlist(req) for req in requests ]
			return render_to_response('html/user.html',
				{"requests":requests,
				 "parts":parts,
				},
				context_instance=RequestContext(request))

