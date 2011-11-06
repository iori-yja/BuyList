from jukai.invt.models import Part
from django.template import Context, loader
from django.http import HttpResponse

def index(request):
	latest_part = Part.objects.all().order_by('id')[:5]
	t = loader.get_template('html/hoge.html')
	c = Context({
		'latest_part': latest_part,
	})
	return HttpResponse(t.render(c))

def update(request,length):
	latest_part = Part.objects.all().order_by('up_date')[:length]
	t = loader.get_template('html/hoge.html')
	c = Context({
		'latest_part': latest_part,
		'update': True,
		'length': length,
	})
	return HttpResponse(t.render(c))

def popular(request):
	latest_part = Part.objects.all().order_by('Hnum')[:10]
	t = loader.get_template('html/hoge.html')
	c = Context({
		'latest_part': latest_part,
		'popular': True,
	})
	return HttpResponse(t.render(c))

def popular(request,length):
	latest_part = Part.objects.all().order_by('Hnum')[:length]
	t = loader.get_template('html/hoge.html')
	c = Context({
		'latest_part': latest_part,
		'popular': True,
		'length': length,
	})
	return HttpResponse(t.render(c))
