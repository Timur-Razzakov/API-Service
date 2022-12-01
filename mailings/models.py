import pytz
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

"""Модель рассылок"""


class Mailing(models.Model):
    date_time_start = models.DateTimeField(verbose_name='Mailing start')
    date_time_end = models.DateTimeField(verbose_name='End of mailing')
    message = models.TextField(verbose_name='Message text')
    mailings_started = models.TimeField(verbose_name='Start time to send message')
    mailings_ended = models.TimeField(verbose_name='End time to send message')
    tag = models.CharField(max_length=120, verbose_name='Search by tags', blank=True)
    mobile_operator = models.CharField(verbose_name='Search by mobile operator',
                                       max_length=3, blank=True)

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

    def __str___(self):
        return self.pk


"""Модель для Клиента"""


class Client(models.Model):
    #  Валидатор для проверки номера телефона
    phone_number_validator = RegexValidator(regex=r'^7\d{10}$',
                                            message="""The format  phone number: 
                                        7XXXXXXXXXX (X - number from 0 to 9)""")

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.CharField(verbose_name='Phone Number', validators=[phone_number_validator],
                                    unique=True,
                                    max_length=11)
    mobile_operator = models.CharField(verbose_name='Mobile operator', max_length=3)
    tag = models.CharField(verbose_name='Search tags', max_length=120, blank=True)
    timezone = models.CharField(verbose_name='Time zone', max_length=255, choices=TIMEZONES, default='UTC')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str___(self):
        return self.pk


"""Модель для сообщений"""


class Message(models.Model):
    time_create = models.DateTimeField(verbose_name='Time create', auto_now_add=True)
    sending_status = models.CharField(verbose_name='Sending status', max_length=15)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_id')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_id')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str___(self):
        return self.pk
