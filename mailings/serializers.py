from rest_framework import serializers
from rest_framework.serializers import Serializer

from .models import Mailing, Client, Message


class GoogleAuth(serializers.Serializer):
    """Сериализация данных от Google """
    email = serializers.EmailField()
    token = serializers.CharField()


class MailingSerializer(serializers.ModelSerializer):
    """Сериализация данных для списка рассылок"""
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    """Сериализация данных для списка клиентов"""
    class Meta:
        model = Client
        fields = "__all__"
    # def create(self, validated_data):
    #     client, _ = Client.objects.update_or_create(
    #         phone_number=validated_data.get('phone_number', None),
    #         mobile_operator=validated_data.get('mobile_operator', None),
    #         tag=validated_data.get('tag', None),
    #         timezone=validated_data.get('timezone', None),
    #     )
    #     return client

class MessageSerializer(serializers.ModelSerializer):
    """Сериализация данных для списка сообщений"""
    class Meta:
        model = Message
        fields = '__all__'

