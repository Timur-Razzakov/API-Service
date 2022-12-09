from django.utils.timezone import now
from rest_framework.test import APITestCase

from mailings.models import Mailing, Client, Message


class TestModel(APITestCase):

    def test_creates_mailings(self):
        mailing = Mailing.objects.create(date_time_start=now(), date_time_end=now(), message='first_test',
                                         mailings_started=now().time(), mailings_ended=now().time(),
                                         tag='test',
                                         )
        self.assertIsInstance(mailing, Mailing)
        self.assertEqual(mailing.tag, 'test')

    #
    def test_creates_clients(self):
        client = Client.objects.create(phone_number='79989999515', mobile_operator='799',
                                       tag='test', timezone='UTC')
        self.assertIsInstance(client, Client)
        self.assertEqual(client.phone_number, '79989999515')

    def test_creates_messages(self):
        self.test_creates_mailings()
        self.test_creates_clients()
        message = Message.objects.create(sending_status='False', mailing_id=2, client_id=2)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.sending_status, 'False')
