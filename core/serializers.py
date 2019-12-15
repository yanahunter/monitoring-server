from rest_framework import serializers
from core.models import Report


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        return Report.objects.create(**validated_data)
