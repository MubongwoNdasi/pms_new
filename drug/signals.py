from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from drug.models import Drugs
from core.models import Pharmacy
from drug.utils import unique_slug_generator


@receiver(pre_save, sender=Drugs)
def create_slug_field(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

