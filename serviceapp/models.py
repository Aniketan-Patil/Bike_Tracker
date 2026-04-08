from django.db import models
from django.contrib.auth.models import User

class ServiceRecord(models.Model):
    bike_model = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    last_serviced_date = models.DateField(null=True, blank=True)  # Keep for service records
    reg_no = models.CharField(max_length=20, default='NA1234')
    progress = models.CharField(max_length=100, blank=True)  # ✅ New field

    def __str__(self):
        return f"{self.bike_model} - {self.owner_name}"


# ✅ New model for under maintenance bikes
class UnderServiceRecord(models.Model):
    service_record = models.ForeignKey(ServiceRecord, on_delete=models.CASCADE)
    issue_description = models.TextField()
    progress = models.CharField(
        max_length=20,
        choices=[
            ('In Progress', 'In Progress'),
            ('Waiting for Parts', 'Waiting for Parts'),
            ('Completed', 'Completed'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_record.reg_no} - {self.progress}"
