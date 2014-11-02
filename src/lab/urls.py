from django.conf.urls import patterns, include, url
from lab import settings
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'lab.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^yeast_libraries/', include('yeast_libraries.urls', namespace='yeast_libraries')),
    url(r'^mediums/', include('mediums.urls', namespace='mediums')),
    url(r'^yeast_liquid_plates/', include('yeast_liquid_plates.urls', namespace='yeast_liquid_plates')),
    
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
