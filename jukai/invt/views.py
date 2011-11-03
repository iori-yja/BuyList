from jukai.invt.models import Part
from django.http import HttpResponse

def index(request):
	latest_part_list = Part.objects.all().order_by('up_date')[:5]
	output = ', '.join([p.name for p in latest_part_list])
	return HttpResponse(output)
