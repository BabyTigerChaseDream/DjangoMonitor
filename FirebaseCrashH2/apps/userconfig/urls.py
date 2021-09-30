from django.urls import path, re_path

from .views import (
	ConfigListView,
	ConfigDetailView,
	ConfigCreateView,
	ConfigUpdateView,
	ConfigDeleteView,
	#ConfigTeamView,
	#TableView,
	crashissues_list,
	crashissues_list_user,
)

from . import views
urlpatterns = [

	# Home dir
	#path('', views.home, name='userconfig-home'),
	# new Home
	path('', views.Filters, name='userconfig-home-with-filter'),

	# defaule view looking for :
	# <app>/<model>_<viewtype>.html
	# blog/config_list.html
	#path('', ConfigListView.as_view(), name='userconfig-home'),

	path('config/<int:pk>/', ConfigDetailView.as_view(), name='config-detail'),
#	# template : <model>_<form>.html -> config_form.html
	path('config/create/', ConfigCreateView.as_view(), name='config-create'),
	path('config/<int:pk>/update/', ConfigUpdateView.as_view(), name='config-update'),
	path('config/<int:pk>/delete/', ConfigDeleteView.as_view(), name='config-delete'),

	#path('config/<int:pk>/delete/', ConfigDeleteView.as_view(), name='config-delete'),

	#path('crashlist/<str:team_id>', views.about, name='userconfig-crashlist'),
	path('crashlist/', views.crashlist, name='userconfig-crashlist'),
	# display crash issues list 
	path('crashdetail/', crashissues_list, name='crash-detail'),
	re_path('crashdetail_user/(?P<userconfig_id>\d+)/$', crashissues_list_user, name='crash-detail-user'),

]
