from django.shortcuts import get_object_or_404
from icecream import ic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from mailings.models import Mailing, Client, Message
from mailings.serializers import MailingSerializer, ClientSerializer, MessageSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """Вывод списка Клиентов"""
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    """Вывод списка Сообщений"""
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    """Вывод списка рассылок"""
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(methods=['get'], detail=True)
    def get_message(self, request, pk=None):
        """ Получаем сообщения, которые привязаны к указанной рассылке и выводим их"""
        mailings = Mailing.objects.all()
        get_object_or_404(mailings, pk=pk)
        get_message = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(get_message, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_total_info(self, request):
        """
        Выводим полную информацию о сообщениях для рассылок
        """
        total_mailings = Mailing.objects.count()
        mailing = Mailing.objects.values('pk')
        content = {'The number of mailings': total_mailings,
                   'The number of messages and their status': ''}
        result = {}
        # для каждой рассылке выводим общую статистику
        for item in mailing:
            ic(item)
            static = {'Total messages': 0, 'Sent': 0, 'No sent': 0}
            all_messages = Message.objects.filter(mailing_id=item['pk']).all()
            group_sent = all_messages.filter(sending_status='True').count()
            group_no_sent = all_messages.filter(sending_status='False').count()
            static['Total messages'] = len(all_messages)
            static['Sent'] = group_sent
            static['No sent'] = group_no_sent
            result[item['pk']] = static

        content['The number of messages and their status'] = result
        return Response(content)
