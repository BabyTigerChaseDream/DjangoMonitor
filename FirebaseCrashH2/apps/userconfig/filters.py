from django.forms.fields import ChoiceField
from .models import Config, PLATFORM_CHOICES
import django_filters
from django import forms



class UserConfigFilter(django_filters.FilterSet):
	# django-filter embed expr
	team = django_filters.CharFilter(lookup_expr='icontains', label='Team', widget=forms.TextInput(attrs={'class': 'input-group input-group-sm'}))
	platform = django_filters.ChoiceFilter(choices=PLATFORM_CHOICES, label='Platform') 

	slack_channel = django_filters.CharFilter(lookup_expr='icontains', label='Slack', widget=forms.TextInput(attrs={'class': 'input-group input-group-sm'})) 
	email_address = django_filters.CharFilter(lookup_expr='icontains', label='Email', widget=forms.TextInput(attrs={'class': 'input-group input-group-sm'}))
	# django-filter customized filter
	#https://stackoverflow.com/questions/57668670/how-to-use-same-same-django-filters-charfilter-field-for-two-separate-fields

	'''
	#https://django-filter.readthedocs.io/en/stable/guide/usage.html
	price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')
	'''
	crash___gt = django_filters.NumberFilter(field_name='crash_count', lookup_expr='gt', label='Mininum Crash Count')
	#crash___lt = django_filters.NumberFilter(field_name='crash_count', lookup_expr='lt')
	user___gt = django_filters.NumberFilter(field_name='total_user', lookup_expr='gt', label='Mininum User Affect')
	#user___lt = django_filters.NumberFilter(field_name='total_user', lookup_expr='lt')

	files = django_filters.CharFilter(lookup_expr='icontains', label='File Names', widget=forms.TextInput(attrs={'class': 'input-group input-group-sm'})) 
	keywords = django_filters.CharFilter(lookup_expr='icontains', label='Keywords in Logs', widget=forms.TextInput(attrs={'class': 'input-group input-group-sm'}))
	#tags = django_filters.CharFilter(lookup_expr='icontains')
