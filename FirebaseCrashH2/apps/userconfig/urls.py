from django.urls import path

from .views import (
	ConfigListView,
	ConfigDetailView,
	ConfigCreateView,
	ConfigUpdateView,
	ConfigDeleteView,
	#ConfigTeamView,
)

from . import views
urlpatterns = [
	path('', views.home, name='userconfig-home'),
	# defaule view looking for :
	# <app>/<model>_<viewtype>.html
	# blog/config_list.html
	path('', ConfigListView.as_view(), name='userconfig-home'),
	path('config/<int:pk>/', ConfigDetailView.as_view(), name='config-detail'),
#	# template : <model>_<form>.html -> config_form.html
	path('config/create/', ConfigCreateView.as_view(), name='config-create'),
	path('config/<int:pk>/update/', ConfigUpdateView.as_view(), name='config-update'),
	path('config/<int:pk>/delete/', ConfigDeleteView.as_view(), name='config-delete'),

	#path('config/<int:pk>/delete/', ConfigDeleteView.as_view(), name='config-delete'),

	#path('crashlist/<str:team_id>', views.about, name='userconfig-crashlist'),
	path('crashlist/', views.crashlist, name='userconfig-crashlist'),

	path('filters/', views.Filters, name='userconfig-filter'),

]
