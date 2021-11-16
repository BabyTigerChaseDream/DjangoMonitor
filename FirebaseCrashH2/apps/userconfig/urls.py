from django.urls import path, re_path
from django.views.generic.base import RedirectView

from .views import (
	#ConfigListView,
	ConfigDetailView,
	ConfigCreateView,
	ConfigUpdateView,
	ConfigDeleteView,
	#ConfigTeamView,
	#TableView,
	crashissues_list,
	crashissues_list_user,
	ignore_issue_id,
	addback_issue_id,
	#crashlist,
	firebase,
	send_notification
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
	#path('listview', ConfigListView.as_view(), name='userconfig-home'),

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

	# ignore issue_id
	re_path('crashdetail_user/(?P<userconfig_id>\d+)/ignore-issue-id/(?P<issue_id_block>\w+)/$', ignore_issue_id, name='ignore-issue-id'),
	# addback issue_id
	re_path('crashdetail_user/(?P<userconfig_id>\d+)/addback-issue-id/(?P<issue_id_addback>\w+)/$', addback_issue_id, name='addback-issue-id'),

	# redirect to firebase for any issue_id
    re_path('firebase/(?P<platform>\w+)/(?P<issue_id>\w+)/$',
        #RedirectView.as_view(url='https://ota.booking.com/crashes/%(platform)s/%(issue_id)s'),
		firebase,
		name='firebase'),

	# redirect to firebase for any issue_id
	re_path('notification/(?P<userconfig_id>\d+)/$', send_notification, name='config-detail-notify'),

]
