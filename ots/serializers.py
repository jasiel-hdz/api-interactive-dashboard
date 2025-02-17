from rest_framework import serializers
from .models import OTS

class OTSDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTS
        fields = ['location_id', 'period_start', 'period_start_date', 'period_start_time', 'ots_count', 'duration', 'watcher_count']        

class OTSSummaryDaySerializer(serializers.Serializer):
    ots_count_sum = serializers.IntegerField()
    ots_count_avg = serializers.FloatField()
    watcher_count_avg = serializers.FloatField()
    watcher_count_total = serializers.IntegerField()
    ots_count = serializers.IntegerField()
    ots = OTSDetailSerializer(many=True)

class DayCountSerializer(serializers.Serializer):
    ots_count = serializers.IntegerField()
    watcher_count = serializers.IntegerField()
    
class OTSSummaryWeekSerializer(serializers.Serializer):
    ots_count_sum = serializers.IntegerField()
    ots_count_avg = serializers.FloatField()
    watcher_count_avg = serializers.FloatField()
    watcher_count_total = serializers.IntegerField()
    ots_count = serializers.IntegerField()
    days = serializers.ListField(child=DayCountSerializer())