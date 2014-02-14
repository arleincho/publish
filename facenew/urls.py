from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',

<<<<<<< HEAD
    url(r'^cancel/', 'facenew.connect.views.cancel', name='cancel'),
    url(r'^admin/', include(admin.site.urls)),
=======
    url(r'^admin/?', include(admin.site.urls)),
>>>>>>> 2f173a15f6c331af961fe9e7d93354c75c3dbd46
    url(r'^fandjango/', include('fandjango.urls')),
    url(r'^$', 'facenew.connect.views.done', name='done'),
    url(r'^cancel/?', 'facenew.connect.views.cancel', name='cancel'),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)