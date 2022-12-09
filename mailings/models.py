import pytz
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

utc = pytz.UTC


class AuthUser(models.Model):
    """ Модель пользователя
    """
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)

    def __str___(self):
        return self.email


class Mailing(models.Model):
    """Рассылки"""
    date_time_start = models.DateTimeField(verbose_name='Mailing start')
    date_time_end = models.DateTimeField(verbose_name='End of mailing')
    message = models.TextField(verbose_name='Message text')
    mailings_started = models.TimeField(verbose_name='Start time to send message')
    mailings_ended = models.TimeField(verbose_name='End time to send message')
    tag = models.CharField(max_length=120, verbose_name='Search by tags', blank=True)
    mobile_operator = models.CharField(verbose_name='Search by mobile operator',
                                       max_length=3, blank=True)

    @property
    def check_date(self):
        """Сравниваем время, для того чтобы знать когда запускать задачу"""
        # start_time = self.date_time_start.replace(tzinfo=utc)
        # end_time = self.date_time_end.replace(tzinfo=utc)
        now = timezone.now()
        if self.date_time_start <= now <= self.date_time_end:
            return True
        else:
            return False

    def __str___(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'

    def __str__(self):
        return f'ID mailing: {str(self.pk)}'


class Client(models.Model):
    """Клиенты"""
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

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f'Customer phone number: {str(self.phone_number)}, ID: {self.pk}'


class Message(models.Model):
    """Сообщения"""
    SENT = "True"
    NO_SENT = "False"

    STATUS_CHOICES = [
        (SENT, "True"),
        (NO_SENT, "False"),
    ]
    time_create = models.DateTimeField(verbose_name='Time create', auto_now_add=True)
    sending_status = models.CharField(verbose_name='Sending status', max_length=15, choices=STATUS_CHOICES, )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='mailing_id')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_id')

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'ID: {str(self.pk)}'
