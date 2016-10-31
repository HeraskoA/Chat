from django.conf.urls import patterns, include, url

from django.contrib import admin
from TestChat import views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'chat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^$', views.home, name='home' ),

	#url(r'^dialog/', views.dialog, name='dialog' ),
	url(r'^dialog/(?P<pk>\d+)/$', views.dialog, name='dialog' ),

url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    url(r'^admin/', include(admin.site.urls)),
)
