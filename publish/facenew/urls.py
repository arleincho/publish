from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'facenew.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^fandjango/', include('fandjango.urls')),
    url(r'^$', 'facenew.connect.views.done', name='done'),
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)