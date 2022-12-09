from rest_framework import serializers

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


class MessageSerializer(serializers.ModelSerializer):
    """Сериализация данных для списка сообщений"""

    class Meta:
        model = Message
        fields = '__all__'
