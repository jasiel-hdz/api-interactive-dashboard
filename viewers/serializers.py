from rest_framework import serializers
from datetime import datetime
from collections import defaultdict
from .models import Viewer

# Serializer for the viewer records
class ViewersSerializer(serializers.ModelSerializer):
    # Method to round the time to the desired format
    def round_time(self, time_str):
        # Convert time from "HH:MM:SS" format to a datetime object
        try:
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            # Round minutes and seconds to zero
            rounded_time = time_obj.replace(minute=0, second=0)
            return rounded_time.strftime('%H:%M:%S')
        except ValueError:
            return time_str

    # Override the representation method to add the rounded time field
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Add a new field 'period_start_time_rounded'
        period_start_time = representation.get('period_start_time', '')
        if period_start_time:
            representation['period_start_time_rounded'] = self.round_time(period_start_time)

        return representation

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
            'age_value',
        ]

# Serializer for the viewer summary
class ViewersSummarySerializer(serializers.Serializer):
    avg_age = serializers.FloatField()
    avg_dwell_time_in_seconds = serializers.FloatField()
    avg_attention_time_in_seconds = serializers.FloatField()
    total_viewers = serializers.IntegerField()
    total_male = serializers.IntegerField()
    total_female = serializers.IntegerField()
    very_happy = serializers.IntegerField()
    happy = serializers.IntegerField()
    neutral = serializers.IntegerField()
    unhappy = serializers.IntegerField()
    very_unhappy = serializers.IntegerField()
    viewers = ViewersSerializer(many=True)

    # Override the representation method to group viewers by rounded hour
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Use a dictionary to group viewers by rounded hour
        grouped_by_hour = defaultdict(int)

        # Group 'viewers' by their rounded hour and count the total for each hour
        for viewer in representation.get('viewers', []):
            period_start_time_rounded = viewer.get('period_start_time_rounded', '')
            if period_start_time_rounded:
                grouped_by_hour[period_start_time_rounded] += 1

        # Create a list of results showing the total viewers for each rounded hour
        viewers_by_hour = []
        for hour, total_viewers in grouped_by_hour.items():
            viewers_by_hour.append({
                'hour': hour,
                'total_viewers': total_viewers
            })

        # Replace the original list of viewers with the list grouped by hour
        representation['viewers'] = viewers_by_hour

        return representation
