from .models import Config
import django_filters

class UserConfigFilter(django_filters.FilterSet):
	# django-filter embed expr
	team = django_filters.CharFilter(lookup_expr='icontains')
	slack_channel = django_filters.CharFilter(lookup_expr='icontains') 
	email_address = django_filters.CharFilter(lookup_expr='icontains')
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
	crash___gt = django_filters.NumberFilter(field_name='crash_count', lookup_expr='gt')
	crash___lt = django_filters.NumberFilter(field_name='crash_count', lookup_expr='lt')
	user___gt = django_filters.NumberFilter(field_name='total_user', lookup_expr='gt')
	user___lt = django_filters.NumberFilter(field_name='total_user', lookup_expr='lt')

	files = django_filters.CharFilter(lookup_expr='icontains') 
	keywords = django_filters.CharFilter(lookup_expr='icontains')
	tags = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Config
		fields = ['team', 'slack_channel', 'email_address']