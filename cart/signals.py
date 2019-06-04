from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver

from drug.models import Drugs

from cart.models import Cart


@receiver(m2m_changed, sender=Cart.drugs.through)
def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        drugs = instance.drugs.all()
        total = 0
        for x in drugs:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


@receiver(pre_save, sender=Cart)
def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.subtotal = 0.00


