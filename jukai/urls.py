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
    url(r'^jukai/$','jukai.invt.views.index'),
    url(r'^jukai/new/','jukai.invt.views.index'),
    url(r'^jukai/new/(\d+)','jukai.invt.views.update'),
    url(r'^jukai/pop/(\d+)','jukai.invt.views.popular'),
)
