from jukai.invt.models import Part
from django.template import Context, loader
from django.http import HttpResponse

def index(request):
	latest_part = Part.objects.all().order_by('up_date')[:5]
	t = loader.get_template('html/hoge.html')
	c = Context({
		'latest_part': latest_part,
	})
	return HttpResponse(t.render(c))
