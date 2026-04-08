from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import UnderServiceRecord

@receiver(post_save, sender=UnderServiceRecord)
def update_service_record_date(sender, instance, **kwargs):
    if instance.progress == 'Completed':
        service_record = instance.service_record
        service_record.last_serviced_date = timezone.now().date()
        service_record.progress = 'Completed'
        service_record.save()
