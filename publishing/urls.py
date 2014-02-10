from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'publishing.connect.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'publishing.connect.views.home'),
    url(r'^logout/$', 'publishing.connect.views.logout'),
    url(r'^done/$', 'publishing.connect.views.done', name='done'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
