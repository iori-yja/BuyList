sed -i 's;/jukai;/django/jukai;g' html/*.html
sed -i 's;/accounts;/django/accounts;g' html/*.html
sed -i "s;HttpResponseRedirect(('/jukai/;HttpResponseRedirect(('/django/jukai/;g" invt/views.py
