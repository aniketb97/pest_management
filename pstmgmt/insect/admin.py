from django.contrib import admin
from .models import Insect, InsectInformation

# Register your models here.
#class InsectAdmin(admin.ModelAdmin):
#    list_display = ['name', 'description']

    # def get_desc(self, instance):
    #     return instance.description
    #
    # get_desc.short_description = 'Description'

class InsectAdmin(admin.ModelAdmin):
    list_display=['insect_name','status','created_by']


class InsectInformationAdmin(admin.ModelAdmin):
    list_display = ['insect_name', 'host_plant', 'host_plant_type', 'lifecycle', 'bionomics', 'shape', 'growth_rate', 'damage', 'symptoms', 'natural_enemies', 'etl', 'size', 'colour', 'species', 'species_example', 'favourable_condition', 'soil_type', 'peak_occurance', 'region', 'reproduction', 'preventive_measures', 'insectiside', 'ipm_techniques', 'speciality']

admin.site.register(Insect, InsectAdmin)
admin.site.register(InsectInformation,InsectInformationAdmin)