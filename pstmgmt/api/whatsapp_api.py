import django
import sys
import os
import traceback
import requests  # to get image from the web
import shutil  # to save it locally
from datetime import datetime

from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from functools import wraps
# from twilio.twiml.voice_response import VoiceResponse
# from twilio.twiml.messaging_response import MessagingResponse

# from twilio.util import RequestValidator
from twilio.request_validator import RequestValidator

# from .models import WorkLog#, WorkDocuments
from logger.logger import Logger
# from MLWork.logger.logger import Logger
# from datetime import datetime as dt
# from django.utils import timezone
# from django.views.decorators.http import require_http_methods

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
log = Logger('Pstmgmt- WhatsAPI')
# Create your views here.
def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.build_absolute_uri(),
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid or settings.DEBUG:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function

# def create_worklog(request, work_desc, created_by, project, work_type, noofmedia):
#     """Create a log."""
#     # import pdb;pdb.set_trace()
#     try:
#         worklog_obj = WorkLog(item_name=work_desc, project=project, item_type=work_type, created_by=created_by)
#         worklog_obj.save()
#         if int(noofmedia)>0:
#             stored_files = storemediafiles(request, noofmedia)
#             for each in stored_files[:1]:
#                 # worklog_doc_pk = worklog_obj.id
#                 # worklog_doc_obj = WorkDocuments()
#                 # worklog_doc_obj.work_id=worklog_obj
#                 worklog_obj.document_path.save("%s" % each[1], File(each[0]))
#                 worklog_obj.save()
#     except Exception as e:
#         log_error(e)
#         return False
#     return True


def get_item_text(incoming_msg, work_type, noofmedia):
    return incoming_msg.strip()
    if incoming_msg.strip() in ['', None]:
        incoming_msg = 'Only Attachment'
    elif incoming_msg.lower().startswith('update'):
        incoming_msg = incoming_msg.strip()
        incoming_msg = incoming_msg.lower().split('update',1)[1]
        if incoming_msg.lstrip().startswith(':'):
            incoming_msg = incoming_msg.lstrip().split(':', 1)[1]
    elif incoming_msg.lower().startswith('event'):
        work_type = 'event'
        incoming_msg = incoming_msg.strip()
        incoming_msg = incoming_msg.lower().split('event',1)[1]
        if incoming_msg.lstrip().startswith(':'):
            incoming_msg = incoming_msg.lstrip().split(':', 1)[1]
    elif incoming_msg.lower().startswith('http'):
        incoming_msg = incoming_msg.strip()
    elif int(noofmedia)>0:  # for pdf attachment,
        incoming_msg = incoming_msg.strip()
    else:
        incoming_msg = 'invalid'
    return incoming_msg, work_type


def get_message(request):
    # import pdb;pdb.set_trace()
    log.set_logger("Info - Message Received. Message Details {}".format(request.POST))
    try:
        incoming_msg = request.POST['Body'] #request.values.get('Body', '').lower()
        msg_from = request.POST['From'] #request.values.get('From', '')
        msg_to = request.POST['To'] #request.values.get('To', '')
        noofmedia = request.POST['NumMedia']
        from_number = msg_from.split('whatsapp:')[1]
        trans_type = 'whatsapp'
        incoming_msg = get_item_text(incoming_msg, trans_type, noofmedia)
        if incoming_msg == 'invalid':
            send_message(request, 'Please give your update.... \n Update: \n Event: ', msg_to, msg_from)
            return HttpResponse('Message Sent!', 200)

        incoming_msg = incoming_msg.strip()
        # create_worklog(request, work_desc, created_by, project, work_type, noofmedia)
        send_message(request, 'Your task logged into system', msg_to, msg_from)
        # Return the TwiML
    except Exception as e:
        log_error(e)
    return HttpResponse('Message Sent!', 200)


def storemediafiles(request, noofmedia):
    # import pdb;pdb.set_trace()
    res = []
    try:
        SmsMessageSid = request.POST['SmsMessageSid']
        for i in range(int(noofmedia)):
            MediaContentType = ''.join(['MediaContentType',str(i)])
            MediaUrl = ''.join(['MediaUrl', str(i)])
            content_type = request.POST[MediaContentType]
            content_type = content_type.lower()
            url = request.POST[MediaUrl]
            extention = content_type.split('/')[1]
            r = requests.get(url, stream=True)
            if r.status_code == 200:

                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
                # print(r.raw.filename)
                # Open a local file with wb ( write binary ) permission.
                # if content_type.startswith('image'):
                filename = '.'.join([str(datetime.timestamp(datetime.now())), extention])
                # filename = os.path.join(settings.BASE_DIR, 'documents', filename)

                # urllib.request.urlretrieve(url,
                #                            "local-filename.jpg")
                #     pass
                # elif content_type.lower().startswith('video'):
                #     pass
                # elif content_type.lower().startswith('application/pdf'):
                #     pass
                # with open(filename, 'wb') as f:
                    # shutil.copyfileobj(r.raw, f)
                data = r.raw._fp.fp.read()
                img_temp = NamedTemporaryFile()
                img_temp.write(data)
                img_temp.flush()
                res.append([img_temp, filename])
                log.set_logger('Info: Image sucessfully Downloaded from {} '.format(url))
            else:
                log.set_logger('Info: Image Couldn\'t be retreived from {} '.format(url))
    except Exception as e:
        log_error(e)
    return res


def getmediafiles(request, noofmedia):
    # import pdb;pdb.set_trace()
    res = []
    try:
        SmsMessageSid = request.POST['SmsMessageSid']

        for i in range(int(noofmedia)):
            MediaContentType = ''.join(['MediaContentType',str(i)])
            MediaUrl = ''.join(['MediaUrl', str(i)])
            content_type = request.POST[MediaContentType]
            content_type = content_type.lower()
            url = request.POST[MediaUrl]
            extention = content_type.split('/')[1]
            # r = requests.get(url, stream=True)
            # if r.status_code == 200:
            #
            #     # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            #     r.raw.decode_content = True
            #     # print(r.raw.filename)
            #     # Open a local file with wb ( write binary ) permission.
            #     # if content_type.startswith('image'):
            #     filename = '.'.join([str(datetime.timestamp(datetime.now())), extention])
            #     # filename = os.path.join(settings.BASE_DIR, 'documents', filename)
            #
            #     # urllib.request.urlretrieve(url,
            #     #                            "local-filename.jpg")
            #     #     pass
            #     # elif content_type.lower().startswith('video'):
            #     #     pass
            #     # elif content_type.lower().startswith('application/pdf'):
            #     #     pass
            #     # with open(filename, 'wb') as f:
            #         # shutil.copyfileobj(r.raw, f)
            #     data = r.raw._fp.fp.read()
            #     img_temp = NamedTemporaryFile()
            #     img_temp.write(data)
            #     img_temp.flush()
            #     res.append([img_temp, filename])
            #     log.set_logger('Info: Image sucessfully Downloaded from {} '.format(url))
            if extention in ['png', 'jpg', 'jpeg']:
                res.append(url)
            else:
                log.set_logger('Info: Image Couldn\'t be retreived from {} '.format(url))
    except Exception as e:
        log_error(e)
    return res


def send_message(request, response_msg, msg_from, msg_to, media_url=None):
    # import pdb;pdb.set_trace()
    try:
        if media_url==None:
            message = client.messages.create(
                                          body=response_msg,
                                          from_=msg_from,
                                          to=msg_to
                                        )
        else:
            message = client.messages.create(
                media_url=[media_url],
                body=response_msg,
                from_=msg_from,
                to=msg_to
            )
        #'Hi!, Jagadisa Here. This is a testing message from Whatsapp',
        # from_ = 'whatsapp:+14155238886',
        # to = 'whatsapp:+918130141308'
        print(message.sid)
    except Exception as e:
        log_error(e)

def send_media_message(request, media_url, response_msg, msg_from, msg_to):
    try:
        message = client.messages.create(
                                      media_url=[media_url],
                                      body=response_msg,
                                      from_=msg_from,
                                      to=msg_to
                                    )
        #'Hi!, Jagadisa Here. This is a testing message from Whatsapp',
        # from_ = 'whatsapp:+14155238886',
        # to = 'whatsapp:+918130141308'
        print(message.sid)
    except Exception as e:
        log_error(e)

def log_error(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_in = repr(traceback.format_tb(exc_traceback)[-1])
    message = ' - '.join(['Error', str(e), error_in])
    log.set_logger(message)


