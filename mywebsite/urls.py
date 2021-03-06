"""mywebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
#from rest_framework.urlpatterns import format_suffix_patterns
from userprofile import views as profileviews
from blogseries import views as blogviews
from rest_framework_jwt.views import obtain_jwt_token


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', profileviews.UserViewSet)
router.register(r'groups', profileviews.GroupViewSet)
router.register(r'profiles', profileviews.ProfileViewSet)
router.register(r'series', blogviews.SeriesViewSet)
router.register(r'blog', blogviews.BlogViewSet)
router.register(r'blogs', blogviews.BlogListViewSet)

#mytestobj = blogviews.BlogViewSet.as_view(REQDICT, lookup_field='slug')
admin.site.site_header = "Bnc Admin"
admin.site.site_title = "Beauty and the Creep Admin"
admin.site.index_title = "Welcome Nigga. There is no return from here."


urlpatterns = [
	url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    #url(r'^edit_profile/', , name='edit_profile'),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='myapp')),	
    url(r'api/all-blogs', blogviews.blog_url_list, name = 'all_blogs'),
    url(r'api/genre-list', blogviews.AllGenresView, name ='all_genres'),
    url(r'api/tag-list', blogviews.AllTagsView, name = 'all_tags'),
    url(r'api/blogresponse', blogviews.UserResponseView, name = 'blog_response'),
    
    #url(r'^api/blogs/(?P<slug>[-\w]+)/$', mytestobj, name = 'blogset')
    #url(r'^api-token-auth/', obtain_jwt_token),	
]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns = format_suffix_patterns(urlpatterns)