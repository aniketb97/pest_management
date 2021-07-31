import sys
import re
import traceback
from background_task import background
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from insect.models import Insect, InsectInformation
from api.models import Transactions, TransactionMedia #, Question #, QuestionTransactions, QuestionTransactionMedia, Transactions, TransactionMedia
from api.whatsapp_api import get_item_text, get_message, send_message, validate_twilio_request, getmediafiles, storemediafiles
from insect.object_detection import get_insects, get_insect_infomation, update_transaction
from logger.logger import Logger
from datetime import datetime
from api.serializers import TransactionSerializer, TransactionMediaSerializer, InsectSerializer, InsectInformationSerializer
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from fuzzywuzzy import fuzz, process


log = Logger('API')
# Create your views here.

def create_transaction(request, incoming_msg, trans_from, noofmedia):
    """Create a log."""
    #import pdb;pdb.set_trace()
    media_obj = []
    try:
        trans_obj = Transactions(trans_type='whatsapp', trans_from=trans_from, trans_msg=incoming_msg)
        trans_obj.save()
        if int(noofmedia)>0:
            stored_files = storemediafiles(request, noofmedia)
            for each in stored_files:
                trans_media_obj = TransactionMedia(transation_fk=trans_obj)
                trans_media_obj.save()
                trans_media_obj.trans_media.save("%s" % each[1], File(each[0]))
                trans_media_obj.save()
                media_obj.append(trans_media_obj)
    except Exception as e:
        log_error(e)
    return media_obj


def update_transaction(insects, trans_media_obj):
    try:
        trans_media_obj.insects = insects
        trans_media_obj.save()
    except Exception as e:
        print(str(e))
    return True


def get_insect_infomation(each_label):
    # import pdb;pdb.set_trace()
    print('Insect Info')
    print(each_label)
    insect_info = InsectInformation.objects.filter(insect_id_fk__insect_name = each_label)
    message = ''
    if len(insect_info)>0:
        insect_info = insect_info[0]
        host_plant = ''.join(['\nHost Plant:\n\t', insect_info.host_plant])
        host_plant_type = ''.join(['\nHost Plant Type:\n\t', insect_info.host_plant_type])

        lifecycle = ''.join(['\nLifecycle:\n\t', insect_info.lifecycle])
        bionomics = ''.join(['\nBionomics:\n\t', insect_info.bionomics])
        shape = ''.join(['\nShape:\n\t', insect_info.shape])
        growth_rate = ''.join(['\nGrowth Rate:\n\t', insect_info.growth_rate])
        damage = ''.join(['\nDamage:\n\t', insect_info.damage])
        symptoms = ''.join(['\nSymptoms:\n\t', insect_info.symptoms])
        natural_enemies = ''.join(['\nNatural Enemies:\n\t', insect_info.natural_enemies])
        etl = ''.join(['\nEconomic Threshold Value:\n\t', insect_info.etl])
        size = ''.join(['\nSize/Length:\n\t', insect_info.size])
        colour = ''.join(['\nColour:\n\t', insect_info.colour])
        species = ''.join(['\nSpecies:\n\t', insect_info.species])
        species_example = ''.join(['\nSpecies Example:\n\t', insect_info.species_example])
        favourable_condition = ''.join(['\nFavourable Condition:\n\t', insect_info.favourable_condition])

        soil_type = ''.join(['\nSoil Type:\n\t', insect_info.soil_type])
        peak_occurance = ''.join(['\nPeak Occurance:\n\t', insect_info.peak_occurance])
        region = ''.join(['\nRegion:\n\t', insect_info.region])
        reproduction = ''.join(['\nReproduction:\n\t', insect_info.reproduction])
        preventive_measures = ''.join(['\nPreventive Measures:\n\t', insect_info.preventive_measures])
        insectiside = ''.join(['\nInsectiside:\n\t', insect_info.insectiside])
        ipm_techniques = ''.join(['\nIntegrated Pest Management Techniqes:\n\t', insect_info.ipm_techniques])
        speciality = ''.join(['\nSpeciality:\n\t', insect_info.speciality])
        print(insect_info.host_plant)
        message = ''.join(
            [host_plant, host_plant_type, lifecycle, bionomics, shape, growth_rate, damage, symptoms, natural_enemies,
             etl, size, colour, species,
             species_example, favourable_condition, soil_type, peak_occurance, region,
             reproduction, preventive_measures, insectiside, ipm_techniques,
             speciality])
        message = '\n\n'.join(
            [each_label.title(), message])
    else:
        print('__________________')
    return message


@require_POST
@csrf_exempt
@validate_twilio_request
def incoming_message(request):
    log.set_logger("Info - Message Received. Message Details {}".format(request.POST))
    try:
        incoming_msg = request.POST['Body'] #request.values.get('Body', '').lower()
        msg_from = request.POST['From'] #request.values.get('From', '')
        msg_to = request.POST['To'] #request.values.get('To', '')
        noofmedia = request.POST['NumMedia']
        from_number = msg_from.split('whatsapp:')[1]
        # incoming_msg, work_type = get_item_text(incoming_msg)
        if incoming_msg.strip() in ['', None] and noofmedia == 0:
            send_message(request, "We didn't find any image.", msg_to, msg_from)
            return HttpResponse('Message Sent!', 200)


        incoming_msg = incoming_msg.strip()
        trans_objs = create_transaction(request, incoming_msg, from_number, noofmedia)
        if not trans_objs == []:
            for each_obj in trans_objs:
                each_url = ''.join([settings.WEBHOST_URL, each_obj.trans_media.url])
                uuid = each_obj.transation_fk.trans_uid
                insects, label = get_insects(each_url, settings.MEDIA_ROOT, from_number, uuid)
                if insects == "":
                    send_message(request, "Didn't find any insect", msg_to, msg_from, each_url)
                else:
                    insect_control_dict = {
                        'aphid':'Aphids suck plant sap, causing foliage to distort and leaves to drop; honeydew excreted on leaves supports sooty mold growth; and feeding spreads viral diseases.\n\nControl these bugs:\n\nWash plants with strong spray of water \nEncourage native predators and parasites such as aphid midges, lacewings, and lady beetles \nWhen feasible, cover plants with floating row covers \nApply hot-pepper or garlic repellent sprays \n',
                        'caterpillar':'Caterpillars are soft, segmented larvae with distinct, harder head capsule with six legs in the front and fleshy false legs on rear segments. They can be found on many fruits and vegetables, ornamentals, and shade trees. Caterpillars chew on leaves or along margins; some tunnel into fruits. \n\nTo deter them:\n\nEncourage native predators and parasites\nHand-pick your harvest\n',
                        'flea beetle':'Flea beetles are small, dark beetles that jump like fleas when disturbed. They hang out on most vegetable crops and are found throughout North America. Adults chew numerous small, round holes into leaves (most damaging to young plants), and larvae feed on plant roots.\n\nFor control:\n\nApply floating row covers\nSpray plants with garlic spray or kaolin clay\n',
                        }
                    # full_message = '\n\n'.join(
                    #     [labels.title(), 'Advisory: This is sample advisory.', 'Suggestion: This is sample suggestion.'])
                    full_message = ''
                    for each_label in label:
                        # try:
                        #     each_message = get_insect_infomation(each_label)
                        #     # each_message = '\n\n'.join(
                        #     #     [each_label.title(), insect_control_dict[each_label]])
                        # except:
                        #     pass
                        try:
                            # get_insect_infomation(each_label)
                            each_message = get_insect_infomation(each_label)
                            if each_message == '':
                                each_message = '\n\n'.join(
                                    [each_label.title(), insect_control_dict[each_label]])
                        except:
                            each_message = '\n'.join(
                                [each_label.title(), 'Details not filled.'])
                        full_message = ''.join(
                                [full_message, each_message, '------------------------------------\n'])
                    update_transaction(insects, each_obj)
                    if len(full_message)> 1600:
                        full_message = full_message[:1600]
                    send_message(request, full_message, msg_to, msg_from, each_url)
        else:
            send_message(request, "Didn't find any image", msg_to, msg_from)

        # Return the TwiML
    except Exception as e:
        log_error(e)
    return HttpResponse('Message Sent!', 200)


def log_error(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_in = repr(traceback.format_tb(exc_traceback)[-1])
    message = ' - '.join(['Error', str(e), error_in])
    log.set_logger(message)


@background(schedule=60)
def prediction(each_url, image_url, trans_from, uuid, trans_media_obj_id):
    # while True:
    print("Started Prediction")
    insects, label = get_insects(each_url, image_url, trans_from, uuid)
    trans_media_obj = TransactionMedia.objects.get(id=trans_media_obj_id)
    trans_media_obj.insects = insects
    trans_media_obj.save()
    # update_insects(insects, trans_media_obj_id)
    print("Ended Prediction")


def get_matched_insects(insect_list, trans_msg):
    try:
        insects = process.extract(trans_msg, insect_list, scorer=fuzz.partial_token_sort_ratio)
    except Exception as e:
        print(str(e))
        return []
    return insects


class CreateTransaction(APIView):
    """
        Mobile Transaction APIs
    """
    permission_classes = (IsAuthenticated,)  # Token Check

    def post(self, request):
        # import pdb;pdb.set_trace()
        resp_message = {'Statuscode': 200, 'data': {"uuid":None, "insect_data":[]}, 'Error': ''}
        try:
            token_key = request.META.get('HTTP_AUTHORIZATION')
            if token_key:
                token_key = token_key[6:]
                user_id = Token.objects.get(key=token_key).user_id
                user = User.objects.get(id=user_id)
                username = user.username
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'Auth Token found empty'
                return resp_message

        except Token.DoesNotExist as e:
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)
            return resp_message

        validated_data = request.data
        import pdb;
        pdb.set_trace()
        try:
            # if
            trans_media = validated_data.get('trans_media')
            trans_from = validated_data.get('trans_from')
            trans_msg = validated_data.get('trans_msg')
            trans_type = validated_data.get('trans_type')
            device_udid = validated_data.get('device_udid')
            device_type = validated_data.get('device_type')

            trans_obj = Transactions.objects.create(trans_from=trans_from, trans_msg=trans_msg, trans_type=trans_type, device_udid=device_udid, device_type=device_type)
            uuid = str(trans_obj.trans_uid)
            if trans_media:
                trans_media_obj = TransactionMedia.objects.create(transation_fk=trans_obj, trans_media=trans_media)
                each_url = ''.join([settings.WEBHOST_URL, trans_media_obj.trans_media.url])
                # insects, label = get_insects(each_url, settings.MEDIA_ROOT, trans_from, uuid)
                # update_transaction(insects, trans_media_obj)
                prediction(each_url, settings.MEDIA_ROOT, trans_from, uuid, trans_media_obj.id)

                resp_message['data']["uuid"]= str(uuid)
                resp_message['Statuscode'] = 200
                resp_message['Error'] = '-'
            elif trans_msg:
                insect_obj = Insect.objects.filter(status='active')
                insect_list = insect_obj.values_list("insect_name", flat=True)
                insects = get_matched_insects(insect_list, trans_msg)

                insect_names = [each_insect for each_insect, ratio in insects if ratio==100 ]
                insects_str = ",".join(insect_names)
                TransactionMedia.objects.create(transation_fk=trans_obj, insects=insects_str)

                insect_informations = InsectInformation.objects.filter(insect_id_fk__in = Insect.objects.filter(insect_name__in = insect_names))
                serializer = InsectInformationSerializer(insect_informations, many=True)

                resp_message['data']["insect_data"] = serializer.data
                resp_message['Statuscode'] = 200
                resp_message['Error'] = '-'
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'We did not process with empty message'
        except Exception as e:
            # log_error(e)
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        return Response(resp_message)

    def get(self, request):
        resp_message = {'Statuscode': 200, 'data': [], 'Error': ''}
        try:
            token_key = request.META.get('HTTP_AUTHORIZATION')
            if token_key:
                token_key = token_key[6:]
                user_id = Token.objects.get(key=token_key).user_id
                user = User.objects.get(id=user_id)
                username = user.username
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'Auth Token found empty'
                return resp_message
        except Token.DoesNotExist as e:
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        try:
            insect_information_list = []
            transactions = TransactionMedia.objects.filter(transation_fk__in=Transactions.objects.filter(trans_from=username))
            for each_trans in transactions:
                insect_information_dict = {'insect_image': None, 'insects': None, 'insect_info': []}
                insect_information_dict['insect_image'] = each_trans.trans_media.url
                insect_information_dict['insects'] = each_trans.insects
                labels = each_trans.insects
                if labels:
                    insect_informations = InsectInformation.objects.filter(
                        insect_id_fk__in=Insect.objects.filter(insect_name__in=labels.split(',')))
                    serializer = InsectInformationSerializer(insect_informations, many=True)
                    insect_information_dict['insect_info'] = serializer.data
                insect_information_list.append(insect_information_dict)

                # serializer = TransactionMediaSerializer(transactions, many=True)
                # insect_information_dict.update(serializer.data)

            resp_message['data'] = insect_information_list
            resp_message['Statuscode'] = 200
            resp_message['Error'] = '-'
        except Exception as e:
            # log_error(e)
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        return Response(resp_message)


class GetTransactionByUUID(APIView):
    """
        Mobile Transaction APIs
    """
    permission_classes = (IsAuthenticated,)  # Token Check

    def post(self, request):

        resp_message = {'Statuscode': 200, 'data': [], 'Error': ''}
        try:
            token_key = request.META.get('HTTP_AUTHORIZATION')
            if token_key:
                token_key = token_key[6:]
                user_id = Token.objects.get(key=token_key).user_id
                user = User.objects.get(id=user_id)
                username = user.username
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'Auth Token found empty'
                return resp_message

        except Token.DoesNotExist as e:
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)
            return resp_message

        # validated_data = request.data
        try:
            uuid = request.data['uuid']
            # uuid = self.request.query_params.get('uuid')
            insect_information_list = []
            if uuid:
                transactions = TransactionMedia.objects.filter(transation_fk=Transactions.objects.get(trans_uid=uuid, trans_from=username))
                if transactions:
                    for each_trans in transactions:
                        insect_information_dict = {'insect_image': None, 'insects': None, 'insect_info': []}
                        insect_information_dict['insect_image'] = each_trans.trans_media.url
                        insect_information_dict['insects'] = each_trans.insects
                        labels = each_trans.insects

                        if labels:
                            insect_informations = InsectInformation.objects.filter(
                                insect_id_fk__in=Insect.objects.filter(insect_name__in=labels.split(',')))
                            serializer = InsectInformationSerializer(insect_informations, many=True)
                            # insect_information_dict.update(serializer.data)
                            insect_information_dict['insect_info'] = serializer.data
                        insect_information_list.append(insect_information_dict)

                resp_message['data'] = insect_information_list
                resp_message['Statuscode'] = 200
                resp_message['Error'] = '-'
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'Invalid parameter value found'

        except Exception as e:
            # log_error(e)
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        return Response(resp_message)


class RegistrationApi(APIView):
    """
        Mobile Transaction APIs
    """
    # permission_classes = (IsAuthenticated,)  # Token Check
    def post(self, request):
        resp_message = {'Statuscode': 200, 'data': {}, 'Error': ''}

        try:
            # first_name = request.data['first_name']
            username = request.data['username']
            if not self.isValid(username):
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = "Invalid username pattern found."
                return Response(resp_message)

            email = request.data.get('email', '')
            password1 = request.data['password1']
            password2 = request.data['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    resp_message['Statuscode'] = 1001
                    resp_message['Error'] = 'User Already Register with {}'.format(username)
                else:
                    try:
                        user = User(username=username, password=password1, email=email)
                        user.save();
                    except Exception as e:
                        resp_message['Statuscode'] = 1001
                        resp_message['Error'] = str(e)
                        return Response(resp_message)
                    else:
                        token = Token.objects.create(user=user)
                        print(token.key)
                        resp_message['Statuscode'] = 200
                        resp_message['Error'] = '-'
                        resp_message['data'] = {'username':username, 'token':token.key}
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'Did not match password and confirm password'
        except Exception as e:
            # log_error(e)
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        return Response(resp_message)

    def isValid(self, s):

        # 1) Begins with 0 or 91
        # 2) Then contains 7 or 8 or 9.
        # 3) Then contains 9 digits
        # Pattern = re.compile("(0/91)?[7-9][0-9]{9}")

        # 1) Then contains 7 or 8 or 9.
        # 2) Then contains 9 digits
        Pattern = re.compile("[7-9][0-9]{9}")
        return Pattern.match(s)

class UserProfileApi(APIView):
    """
        Mobile Transaction APIs
    """
    permission_classes = (IsAuthenticated,)  # Token Check

    def get(self, request):
        resp_message = {'Statuscode': 200, 'data': {}, 'Error': ''}
        token_key = request.META.get('HTTP_AUTHORIZATION')
        # if token_key:
        token_key = token_key[6:]
        user_id = Token.objects.get(key=token_key).user_id

        try:
            if user_id:
                user_data = User.objects.get(id=user_id)
                if user_data:
                    # data = {'email':''}
                    resp_message['data'] = {'username': user_data.username,'email': user_data.email}
                    resp_message['Statuscode'] = 200
                    resp_message['Error'] = '-'
                else:
                    resp_message['Statuscode'] = 1001
                    resp_message['Error'] = 'No user found'
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'username can be empty string'
        except Exception as e:
            # log_error(e)
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        return Response(resp_message)


class LoginUserApi(APIView):
    """
        Mobile Transaction APIs
    """
    # permission_classes = (IsAuthenticated,)  # Token Check

    def post(self, request):
        resp_message = {'Statuscode': 200, 'data': {}, 'Error': ''}
        import pdb;pdb.set_trace()
        try:
            # first_name = request.data['first_name']

            username = request.data['username']
            password = request.data['password']

            if username and password:
                try:
                    user = authenticate(username=username, password=password)
                    if user:
                        try:
                            token = Token.objects.get(user=user)
                        except Token.DoesNotExist as e:
                            # resp_message['Error'] = str(e)
                            resp_message['Statuscode'] = 1001
                            resp_message['Error'] = 'No Token Found for this user. Please check with Administrator.'
                        else:
                            resp_message['Statuscode'] = 200
                            resp_message['Error'] = '-'
                            resp_message['data'] = {'username': username, 'token': token.key}
                    else:
                        resp_message['Statuscode'] = 1001
                        resp_message['Error'] = 'Inactive User Found.'
                except Exception as e:
                    resp_message['Statuscode'] = 1001
                    resp_message['Error'] = str(e)
                    return Response(resp_message)
            else:
                resp_message['Statuscode'] = 1001
                resp_message['Error'] = 'Username and password can not be empty'
        except Exception as e:
            # log_error(e)
            resp_message['Statuscode'] = 1001
            resp_message['Error'] = str(e)

        return Response(resp_message)
