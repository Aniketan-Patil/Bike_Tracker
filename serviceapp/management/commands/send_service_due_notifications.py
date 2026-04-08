import os
import django

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biketracker3.settings')

# Initialize Django
django.setup()

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from serviceapp.models import ServiceRecord
from serviceapp.sms_notifications import send_sms

class Command(BaseCommand):
    help = 'Send SMS notifications for service due records'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now().date() - timedelta(days=90)
        records = ServiceRecord.objects.filter(last_serviced_date__lte=cutoff_date)

        if not records.exists():
            self.stdout.write(self.style.SUCCESS("No service due records found."))
            return

        for record in records:
            message = (
                f"Reminder: Your bike model {record.bike_model} "
                f"(Reg No: {record.reg_no}) is due for service."
            )
            try:
                send_sms(record.contact, message)
                self.stdout.write(self.style.SUCCESS(
                    f"✅ Sent SMS to {record.contact} for record ID {record.id}"
                ))
            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f"❌ Failed to send SMS to {record.contact} (ID {record.id}): {str(e)}"
                ))
