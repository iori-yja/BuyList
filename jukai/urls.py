from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jukai.views.home', name='home'),
    # url(r'^jukai/', include('jukai.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'jukai/admin/', include(admin.site.urls)),
    url(r'^jukai/(\d+)','jukai.invt.views.editor'),
    url(r'^jukai/$','jukai.invt.views.index'),
    url(r'^jukai/new/(\d+)','jukai.invt.views.new'),
    url(r'^jukai/new/','jukai.invt.views.new'),
    url(r'^jukai/pop/(\d+)','jukai.invt.views.popular'),
    url(r'^jukai/pop/','jukai.invt.views.popular'),
    url(r'^jukai/add/$','jukai.invt.views.partadd'),
    url(r'^jukai/add/(.+)','jukai.invt.views.partadd'),
    url(r'^jukai/reqs/$','jukai.invt.views.listreqs'),
    url(r'^jukai/req/(\d+)','jukai.invt.views.request'),
   #url(r'^jukai/delete/(\d+)', 'jukai.invt.views.delete'),
   # url(r'^jukai/cancel/(\d+)', 'jukai.invt.views.cansel'),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'html/lin.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
