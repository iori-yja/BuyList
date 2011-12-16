from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
import operator
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from jukai.invt.models import *
from django.http import HttpResponse


def mkprop(part):
	try: prop=part.resistor.mkprop
	except:
		try: prop=part.wiring.mkprop
		except:
			try: prop=part.capasitor.mkprop
			except:
				try: prop=part.motor.mkprop
				except:
					try: prop=part.mcu.mkprop
					except:
						try: prop=part.material.mkprop
						except:
							try: prop=part.motor_driver.mkprop
							except:
								try: prop=part.switch.mkprop
								except:
									try: prop=part.regulater.mkprop
									except:
										try: prop=part.subtrace.mkprop
										except:
											try: prop=part.connector.mkprop
											except:
												try: prop=part.other.mkprop
												except: prop="><"
	return prop

class Parter:
	def __init__(self, latest_part):
		self.latest_part = latest_part
		all_req = self.latest_part.req_set.all()[:10]
		self.up_date = 0
		self.prop = mkprop(latest_part)
		if all_req:	self.up_date = all_req[0].up_date
		else:		self.up_date = 'Not yet'
		if self.latest_part.req_set.all()[:10]:
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


class Nudes:
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
		self.up_date = latest_req.up_date
		self.allneeds   = latest_req.allneeds   
		self.Mlevneeds  = latest_req.Mnum  
		self.Alevneeds  = latest_req.Anum  
		self.Blevneeds  = latest_req.Bnum  
		self.Clevneeds  = latest_req.Cnum  


def listreqs(request):
	latest_req_list = Req.objects.all().order_by('-up_date')
	nee = [ Reqlist(latest_req) for latest_req in latest_req_list ]
	return render_to_response('html/hoge.html',
		{'needs': nee},
		context_instance=RequestContext(request))

def index(request):
	latest_part_list = Part.objects.all().order_by('id')[:1000]
	nee = [ Parter(latest_part) for latest_part in latest_part_list ]
	return render_to_response('html/hoge.html',
		{'needs': nee},
		context_instance=RequestContext(request))


def new(request,length=10000):
	latest_req_list = Req.objects.all().order_by('-up_date')[:length]
	nee = [ Nudes(latest_req) for latest_req in latest_req_list ]
	nee = reduce( lambda xs,y: xs if filter(lambda x:x.latest_part==y.latest_part,xs) else xs+[y], nee, [])
	return render_to_response('html/hoge.html',
		{'needs': nee,
		'update': True,
		'length': length},
		context_instance=RequestContext(request)
		)

def popular(request,length=10000):
	latest_part_list = Part.objects.all().order_by('id')[:length]
	nee = [ Parter(latest_part) for latest_part in latest_part_list ]
	new = sorted(nee,reverse=True,key=operator.attrgetter('allneeds'))
	return render_to_response('html/hoge.html',
		{'needs': new,
		'update': True,
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

def getform(sp):
	if( sp == 'resis'):
		Form = ResistorForm()
	if( sp == 'wire'):
		Form = WiringForm()
	if( sp == 'motor'):
		Form = MotorForm()
	if( sp == 'capas'):
		Form = CapasitorForm()
	if( sp == 'motod'):
		Form = Motor_driverForm()
	if( sp == 'switch'):
		Form = SwitchForm()
	if( sp == 'reg'):
		Form = RegulaterForm()
	if( sp == 'mat'):
		Form = MaterialForm()
	if( sp == 'subt'):
		Form = SubtraceForm()
	if( sp == 'mcu'):
		Form = McuForm()
	if( sp == 'con'):
		Form = ConnectorForm()
	if( sp == 'other'):
		Form = OtherForm()
	return Form

def getformwitharg(sp,*arg,**kwarg):
	if( sp == 'resis'):
		Form = ResistorForm(*arg,**kwarg)
	if( sp == 'wire'):
		Form = WiringForm(*arg,**kwarg)
	if( sp == 'motor'):
		Form = MotorForm(*arg,**kwarg)
	if( sp == 'capas'):
		Form = CapasitorForm(*arg,**kwarg)
	if( sp == 'motod'):
		Form = Motor_driverForm(*arg,**kwarg)
	if( sp == 'switch'):
		Form = SwitchForm(*arg,**kwarg)
	if( sp == 'reg'):
		Form = RegulaterForm(*arg,**kwarg)
	if( sp == 'mat'):
		Form = MaterialForm(*arg,**kwarg)
	if( sp == 'subt'):
		Form = SubtraceForm(*arg,**kwarg)
	if( sp == 'mcu'):
		Form = McuForm(*arg,**kwarg)
	if( sp == 'con'):
		Form = ConnectorForm(*arg,**kwarg)
	if( sp == 'other'):
		Form = OtherForm(*arg,**kwarg)
	return Form

def getobj(sp):
	if( sp == 'resis'):
		obj = Resistor()
	if( sp == 'wire'):
		obj = Wiring()
	if( sp == 'motor'):
		obj = Motor()
	if( sp == 'capas'):
		obj = Capasitor()
	if( sp == 'motod'):
		obj = Motor_driver()
	if( sp == 'switch'):
		obj = Switch()
	if( sp == 'reg'):
		obj = Regulater()
	if( sp == 'mat'):
		obj = Material()
	if( sp == 'subt'):
		obj = Subtrace()
	if( sp == 'mcu'):
		obj = Mcu()
	if( sp == 'con'):
		obj = Connector()
	if( sp == 'other'):
		obj = Other()
	return obj


def partadd(request,sp='none'):
	if request.user.is_authenticated():
		if sp != 'none': partobj = getobj(sp)
		if request.method == 'POST':
			new_part = getformwitharg(sp,request.POST,instance=partobj)
			if new_part.is_valid():
				new_part.save()
				return HttpResponseRedirect('/registered')
			else:
				return HttpResponseRedirect('/Oops')
		else:
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
		if request.method == 'POST':
			update_req = ReqForm(request.POST,instance=reqobj)
			if update_req.is_valid():
				update_req.save()
				return HttpResponseRedirect('/jukai')
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


#def delete(request,kind,id):
#	if request.user.is_authenticated():
#		partobj = Part.objects.get(id=part_id)
#		partobj.delete()
#		return HttpResponseRedirect('/jukai')
#	else:
#		return HttpResponseRedirect('/Oops')
#
