from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Mailing, Client, Message
from .tasks import send_message


# декоратор, для получения сигнала о том, что произошло сохранение новой рассылки
@receiver(post_save, sender=Mailing, dispatch_uid="message")
def listen_mailing_and_create_message(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(mobile_operator=mailing.mobile_operator,
                                        tag=mailing.tag).all()
        for client in clients:
            #  Перебирая клиентов и создаём новое сообщение
            Message.objects.create(
                sending_status="False",
                client_id=client.id,
                mailing_id=instance.id
            )
            message = Message.objects.filter(mailing_id=instance.id, client_id=client.id).first()
            # определяем переменные для отправки во внешний сервис
            client_id = client.id
            mailing_id = mailing.id
            data = {
                'id': message.id,
                'phone': client.phone_number,
                'text': mailing.message
            }
            if instance.check_date:
                send_message.apply_async((data, client_id, mailing_id),
                                         expires=mailing.date_time_end)
            else:
                send_message.apply_async((data, client_id, mailing_id),
                                         eta=mailing.date_time_start, expires=mailing.date_time_end)
