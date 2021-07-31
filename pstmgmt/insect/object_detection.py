import cv2
import numpy as np
import os
from pathlib import Path
from urllib.request import urlopen
from insect.models import InsectInformation
# from api.serializers import Transactions,TransactionMediaSerializer

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    # import pdb;
    # pdb.set_trace()
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    # return the image
    return image


def get_insects(path, media_root, from_number, uuid):
    #import pdb;pdb.set_trace()
    weight_file = os.path.join(os.path.dirname(__file__), 'yolov3_training_10000.weights')
    cfg_file = os.path.join(os.path.dirname(__file__), 'yolov3_testing.cfg')
    net = cv2.dnn.readNet(weight_file, cfg_file)
    classes = []
    with open(os.path.join(os.path.dirname(__file__), 'classes.txt'),'r') as f:
        classes = f.read().splitlines()

    #img = cv2.imread('C:/Users/Lenovo/Desktop/yolov3/Test_Images/spider6.jpg')
    img = url_to_image(path)#cv2.imread(path)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

    # for b in blob:
    #     for n, img_blob in enumerate(b):
    #         cv2.imshow(str(n), img_blob)

    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes=[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    #print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    # print(indexes.flatten())
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    insects = ""
    label = []
    if len(indexes) > 0:
        # import pdb;
        # pdb.set_trace()
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            class_name = str(classes[class_ids[i]])
            if class_name not in label:
                label.append(class_name)

            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            print(label)
            cv2.putText(img, class_name + " " + confidence, (x, y+20), font, 2, (0, 255, 0), 2)

        insects = ', '.join(label)
    #import pdb;pdb.set_trace()
    basename = os.path.basename(path)
    ext = Path(basename).suffix
    name = ''.join(['output', ext])
    filename = os.path.join(media_root, 'insects', from_number, str(uuid), 'images', name)
    cv2.imwrite(filename, img)
    # with open(filename, 'wb') as f:
    #     f.write(img)
    return insects, label
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



def detect(insects, trans_media):
    try:
        trans_media.insect=insects
        trans_media.save()
    except Exception as e:
        print(str(e))
    return True

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


def get_insects_app(path, media_root, uuid):
    #import pdb;pdb.set_trace()
    weight_file = os.path.join(os.path.dirname(__file__), 'yolov3_training_10000.weights')
    cfg_file = os.path.join(os.path.dirname(__file__), 'yolov3_testing.cfg')
    net = cv2.dnn.readNet(weight_file, cfg_file)
    classes = []
    with open(os.path.join(os.path.dirname(__file__), 'classes.txt'),'r') as f:
        classes = f.read().splitlines()

    #img = cv2.imread('C:/Users/Lenovo/Desktop/yolov3/Test_Images/spider6.jpg')
    img = url_to_image(path)#cv2.imread(path)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)

    # for b in blob:
    #     for n, img_blob in enumerate(b):
    #         cv2.imshow(str(n), img_blob)

    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes=[]
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    #print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
    # print(indexes.flatten())
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))
    insects = ""
    label = []
    if len(indexes) > 0:
        # import pdb;
        # pdb.set_trace()
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            class_name = str(classes[class_ids[i]])
            if class_name not in label:
                label.append(class_name)

            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            print(label)
            cv2.putText(img, class_name + " " + confidence, (x, y+20), font, 2, (0, 255, 0), 2)

        insects = ', '.join(label)
    #import pdb;pdb.set_trace()
    basename = os.path.basename(path)
    ext = Path(basename).suffix
    name = ''.join(['output', ext])
    filename = os.path.join(media_root, 'insects', str(uuid), 'images', name)
    cv2.imwrite(filename, img)
    # with open(filename, 'wb') as f:
    #     f.write(img)
    return insects, label
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
