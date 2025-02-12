from rest_framework import viewsets
from rest_framework import serializers
from .models import OTS

class OTSSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTS
        fields = '__all__'