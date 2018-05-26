from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'waterapp'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('about', views.about),
	path('services', views.services.as_view(), name = 'services'),
	path('introduce', views.introduce),
    path('agree', views.agree, name = 'agree'),
	path('login/', auth_views.login, {'template_name': 'waterapp/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': 'login'}, name='logout'),
    path('accounts/signup/', views.signup.as_view(), name='signup'),
  	path('post_list', views.postLV.as_view(), name='post_list'),
    path(r'post/(<pk>\d+)/', views.post_detail, name='post_detail'),
    path(r'post/new/', views.post_new, name='post_new'),
    path(r'post/(<pk>\d+)/edit/', views.post_edit, name='post_edit'),
    path(r'post/(<pk>\d+)/remove/', views.post_remove, name='post_remove'),
    path(r'comment/(<pk>\d+)/remove/', views.comment_remove, name='comment_remove'),
    path(r'comment/(<pk>\d+)/edit/', views.comment_edit, name='comment_edit'),
    path('post1_list', views.post1LV.as_view(), name='post1_list'),
    path(r'post1/(<pk>\d+)/', views.post1_detail, name='post1_detail'),
    path(r'post1/new/', views.post1_new, name='post1_new'),
    path(r'post1/(<pk>\d+)/edit/', views.post1_edit, name='post1_edit'),
    path(r'post1/(<pk>\d+)/remove/', views.post1_remove, name='post1_remove'),
    path(r'comment1/(<pk>\d+)/remove/', views.comment1_remove, name='comment1_remove'),
    path(r'comment1/(<pk>\d+)/edit/', views.comment1_edit, name='comment1_edit'),
    path('post2_list', views.post2LV.as_view(), name='post2_list'),
    path(r'post2/(<pk>\d+)/', views.post2_detail, name='post2_detail'),
    path(r'post2/new/', views.post2_new, name='post2_new'),
    path(r'post2/(<pk>\d+)/edit/', views.post2_edit, name='post2_edit'),
    path(r'post2/(<pk>\d+)/remove/', views.post2_remove, name='post2_remove'),
    path(r'comment2/(<pk>\d+)/remove/', views.comment2_remove, name='comment2_remove'),
    path(r'comment2/(<pk>\d+)/edit/', views.comment2_edit, name='comment2_edit'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name = 'activate'),
    path(r'duplcheck', views.DuplicationCheck.as_view(), name='duplcheck'),
    path(r'password/', views.change_password, name='change_password'),
    path(r'password_reset/', auth_views.password_reset,{'template_name': 'waterapp/password_reset_form.html'} ,name='password_reset'),
    path(r'password_reset/done/',  auth_views.password_reset_done,{'template_name': 'waterapp/password_reset_done.html'},name='password_reset_done'),
    path(r'reset/<uidb64>/<token>/', auth_views.password_reset_confirm,{'template_name': 'waterapp/password_reset_confirm.html'} ,name='password_reset_confirm'),
    path(r'reset/done/',auth_views.password_reset_complete,{'template_name': 'waterapp/password_reset_complete.html'} , name='password_reset_complete')
]
