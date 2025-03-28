from rest_framework import serializers

class RequestDataSerializer(serializers.Serializer):
    ServerID = serializers.CharField()
    Start = serializers.CharField()
    End = serializers.CharField()