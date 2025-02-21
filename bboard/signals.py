from django.db.models.signals import post_save
from django.dispatch import receiver

from bboard.models import Bb

@receiver(post_save, sender=Bb)
def post_save_dispatcher(sender, **kwargs):
    snd = sender
    print(f'Создаём объявление в модели {snd}')

    if isinstance or kwargs['instance']:
    instance = kwargs['instance']
    instance.title = instance.title.capitalize()
    print(f'Создали объявление с заголовком {instance.title}')


post_save.connect(post_save_dispatcher)
post_save.connect(post_save_dispatcher, sender=Bb)
post_save.connect(post_save_dispatcher, dispatch_uid='post_save_dispatcher_1')
post_save.connect(post_save_dispatcher, dispatch_uid='post_save_dispatcher_2')



