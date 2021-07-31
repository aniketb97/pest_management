from django.db import models
import django
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]

INSECT_PROCESS_STATUS = [
    ('created', 'Created'),
    ('approved', 'Approved'),
    ('labelled', 'Labelled'),
    ('trained', 'Trained'),
]

class Insect(models.Model):
    insect_name = models.CharField(max_length=100)
    process_status = models.CharField(max_length=100, choices=INSECT_PROCESS_STATUS, default='created')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    creation_date = models.DateField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insect_creater')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insect_approver')
    approved_on = models.DateField(blank=True, default=django.utils.timezone.now)

    def __str__(self):
        return self.insect_name

    class Meta:
        db_table = "insect_master"


from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#class Insect(models.Model):
#   name = models.CharField(max_length=256)
#   description = models.CharField(max_length=1024, default=None, blank=True)
#   active = models.BooleanField(default=True)
#   creation_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
#   creation_by = models.ForeignKey(User, on_delete=models.CASCADE)

#    def __str__(self):
#        return self.name

APPPROVED_STATUS = [
    ('created', 'Created'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
]

class InsectInformation(models.Model):
    insect_id_fk = models.OneToOneField(Insect, on_delete=models.CASCADE)
    host_plant = models.TextField()
    host_plant_type = models.CharField(max_length=500)
    lifecycle = models.TextField()
    bionomics = models.TextField()
    shape = models.TextField()
    growth_rate = models.CharField(max_length=500)
    damage = models.TextField()
    symptoms = models.TextField()
    natural_enemies = models.CharField(max_length=500)
    etl = models.CharField(max_length=500)
    size = models.CharField(max_length=500)
    colour = models.CharField(max_length=500)
    species = models.CharField(max_length=500)
    species_example = models.CharField(max_length=500)
    favourable_condition = models.TextField()
    soil_type = models.CharField(max_length=500)
    peak_occurance = models.CharField(max_length=500)
    region = models.CharField(max_length=500)
    reproduction = models.TextField()
    preventive_measures = models.TextField()
    insectiside = models.TextField()
    ipm_techniques = models.TextField()
    speciality = models.CharField(max_length=500)
    creation_date = models.DateField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info_creater')
    approve_status = models.CharField(max_length=100, choices=APPPROVED_STATUS, default='created')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='info_approver')
    approved_on = models.DateField(blank=True, default=django.utils.timezone.now)
    # def __str__(self):
    #     return self.host_plant


    class meta:
        db_table = "insect_information"