from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APITestCase
from mailings.models import Mailing, Message, Client


class TestStat(APITestCase):

    def test_mailing(self):
        mail_count = Mailing.objects.all().count()
        mail_create = {"date_time_start": now(), "date_time_end": now(), 'mailings_started': now().time(),
                       'mailings_ended': now().time(), "message": "first_test", "tag": "test",
                       "mobile_operator": '799'}
        response = self.client.post('http://127.0.0.1:8000/v1/mailings/', mail_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mailing.objects.all().count(), mail_count + 1)
        self.assertEqual(response.data['message'], 'first_test')
        self.assertIsInstance(response.data['message'], str)
    #
    def test_client(self):
        client_count = Client.objects.all().count()
        client_create = {"phone_number": '79989999656',
                         "tag": "test", "timezone": "UTC",
                         "mobile_operator":'798'}
        response = self.client.post('http://127.0.0.1:8000/v1/clients/', client_create)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.all().count(), client_count + 1)
        self.assertEqual(response.data['phone_number'], '79989999656')
        self.assertIsInstance(response.data['phone_number'], str)

    def test_message(self):
        response = self.client.get('http://127.0.0.1:8000/v1/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stat(self):
        self.test_mailing()
        url = 'http://127.0.0.1:8000/v1/mailings'
        response = self.client.get(f'{url}/4/get_message/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f'{url}/2/get_message/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(f'{url}/get_total_info/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['The number of mailings'], 1)
        self.assertIsInstance(response.data['The number of mailings'], int)
        self.assertIsInstance(response.data['The number of messages and their status'], dict)
