"""
otasmusic URL Configuration

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
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from config import settings
from otasmusic.views import SongDetailView, RecordListView, HomePageView, PersonDetailView, RecordDetailView, PersonListView, \
    RecentView, BandDetailView, AlbumDetailView, EventDetailView, ServicesView, ContactView, CalendarView


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # re_path(r'^login/$', auth_views.login, name='login'),
    # re_path(r'^logout/$', auth_views.logout_then_login, name='logout'),
    # re_path(r'^signup/$', UserSignUpView.as_view(), name='signup'),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    # re_path(r'contact/?$', ContactView.as_view(), name='contact'),
    # re_path(r'contact/calendar/?$', CalendarView.as_view(), name='calendar'),
    # re_path(r'services/?$', ServicesView.as_view(), name='services'),
    re_path(r'record/(?P<slug>[\w-]+)/?$', RecordDetailView.as_view(), name='record'),
    re_path(r'song/(?P<slug>[\w-]+)/?$', SongDetailView.as_view(), name='song'),
    re_path(r'person/(?P<slug>[\w-]+)/?$', PersonDetailView.as_view(), name='person'),
    # re_path(r'records/?$', RecordListView.as_view(), name="records"),
    # re_path(r'persons/?$', PersonListView.as_view(), name="persons"),
    # re_path(r'recent/?$', RecentView.as_view(), name="recent"),
    re_path(r'band/(?P<slug>[\w-]+)/?$', BandDetailView.as_view(), name='band'),
    re_path(r'album/(?P<slug>[\w-]+)/?$', AlbumDetailView.as_view(), name='album'),
    # url(r'event/(?P<pk>\d+)/?$', EventDetailView.as_view(), name='event'),
    re_path(r'^$', HomePageView.as_view(), name="home"),
]

if settings.DEBUG:
    urlpatterns += [
        re_path('__debug__/', include('debug_toolbar.urls'))
    ]
