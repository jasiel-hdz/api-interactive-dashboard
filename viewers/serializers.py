from rest_framework import serializers
from .models import Viewer

# Create your views here.
class ViewersSerializer(serializers.ModelSerializer):
        class Meta:
            model = Viewer
            fields = [
            'location_id',
            'period_start',
            'period_start_date',
            'period_start_time',
            'very_happy',
            'happy',
            'neutral',
            'unhappy',
            'very_unhappy',
            'gender',
            'age',
            'dwell_time_in_tenths_of_sec',
            'attention_time_in_tenths_of_sec',
            'age_value'
        ]