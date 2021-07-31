from django.conf import settings
from .models import Transactions, TransactionMedia
from insect.models import Insect, InsectInformation
from rest_framework import serializers, request
# from insect.object_detection import get_insects, update_transaction
# from api.models import Transactions, TransactionMedia


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = ('trans_from','trans_type','trans_msg')


class TransactionMediaSerializer(serializers.ModelSerializer):
    transation_fk = TransactionSerializer()

    class Meta:
        model = TransactionMedia
        fields = ('insects','trans_media','transation_fk')
        read_only_fields = ['insects','transation_fk']


class InsectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insect
        fields = ('insect_name','process_status','status', 'created_by', 'approved_by')


class InsectInformationSerializer(serializers.ModelSerializer):
    insect_id_fk = InsectSerializer()

    class Meta:
        model = InsectInformation
        fields = ('host_plant','host_plant_type','lifecycle','bionomics','shape',
                  'growth_rate','damage','symptoms', 'natural_enemies','etl','size',
                  'colour','species','species_example','favourable_condition','soil_type','peak_occurance',
                  'region','reproduction', 'preventive_measures','insectiside','ipm_techniques','speciality',
                  'creation_date','approve_status',
                  'approved_by','approved_on', 'insect_id_fk')
        read_only_fields = ['insect_id_fk']






