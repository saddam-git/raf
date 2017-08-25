"""raf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from tag.views import TagList,TagCreate,TagDelete,TagUpdate,TagDetail
from django.views.generic import TemplateView,RedirectView
from user import urls as user_urls


urlpatterns = [
    url(r'^$',
        RedirectView.as_view(pattern_name ='tag_list_view',
        permanent = False)),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/$',TemplateView.as_view(template_name='blog/post_list.html'),name='post_list'),
    url(r'^tag/$',TagList.as_view(),name = 'tag_list_view'),
    url(r'^tag/create/$',TagCreate.as_view(),name='tag_create'),
    url(r'^tag/(?P<slug>[\w-]+)/delete/$',TagDelete.as_view(),name='tag_delete'),
    url(r'^tag/(?P<slug>[\w-]+)/detail/$',TagDetail.as_view(),name='tag_detail'),
    url(r'^tag/(?P<slug>[\w-]+)/update/$',TagUpdate.as_view(),name='tag_update'),

    url(r'^user/',include(user_urls,app_name='user',namespace='dj-auth')),



]
