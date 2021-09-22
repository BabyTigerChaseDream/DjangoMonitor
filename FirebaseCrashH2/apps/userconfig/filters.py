from .models import Config
import django_filters

class UserConfigFilter(django_filters.FilterSet):
    class Meta:
        model = Config
        fields = ['team', 'slack_channel', 'crash_count']