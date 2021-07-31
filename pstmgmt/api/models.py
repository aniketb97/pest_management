import random
import string
import uuid
import django
from django.db import models
from pathlib import Path

API_TRANS_TYPE = [
    ('whatsapp', 'whatsapp'),
    ('app', 'app')
]



# Create your models here.
class Transactions(models.Model):
    trans_uid = models.UUIDField(default=uuid.uuid4, editable=False)
    trans_type = models.CharField(choices=API_TRANS_TYPE, max_length=16)
    trans_from = models.CharField(default='', max_length=36)
    trans_msg = models.CharField(default='', max_length=256)
    trans_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    device_udid = models.CharField(default='1111111111111111111111111111111111111111', max_length=64)
    device_type = models.CharField(default='', max_length=64)



class TransactionMedia(models.Model):
    def get_image_path(instance, filename):
        if filename:
            random_char = ''.join([random.choice(string.ascii_letters
                                                 + string.digits) for n in range(6)])
            basename = Path(filename).stem
            ext = Path(filename).suffix
            new_basename = '_'.join([basename, random_char])
            filename = ''.join([new_basename, ext])
        if not instance.transation_fk.trans_from:
            trans_from = 'common'
        else:
            trans_from = instance.transation_fk.trans_from
        url = 'insects/{0}/{1}/images/{2}'.format(trans_from, instance.transation_fk.trans_uid, filename)
        return url

    transation_fk = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    trans_media = models.ImageField(upload_to=get_image_path, blank=True)
    insects = models.CharField(max_length=128, default='')


# SEQUENCE = [
#     (1, 1),
#     (2, 2),
#     (3, 3),
#     (4, 4),
#     (5, 5)
# ]

# Create your models here.
# class Question(models.Model):
#     question = models.CharField(max_length=512)
#     sequence = models.CharField(choices=SEQUENCE, max_length=3)
#     active = models.BooleanField(default=True)

