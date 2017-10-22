# -*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
# post views
    url(r'^$', views.post_list, name='post_list'),
    #url(r'^$', views.PostListView.as_view(),name='post_list'),
    url(r'^blog/tag/(?P<tag_slug>[-\w]+)/$',views.post_list,name='post_list_by_tag'),

    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/(?P<id>\d+)/$',
                    views.post_detail,
                    name='post_detail'),

    url(r'^blog/(?P<post_id>\d+)/share/$',views.post_share,name='post_share'),
    url(r'^music/$',views.music,name='music'),
    url(r'^login/$',views.userLogin,name="user_login"),
    url(r'^logout/$',views.userLogout,name="user_logout"),
    url(r'^register/$', views.userRegister, name="user_register"),
]