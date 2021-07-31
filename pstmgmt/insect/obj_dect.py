import cv2
import numpy as np
from urllib.request import urlopen

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    # return the image
    return image

def get_insects(path):
    import pdb;pdb.set_trace()
    net = cv2.dnn.readNet('yolov3_training_10000.weights', 'yolov3_testing.cfg')
    classes = []
    with open('classes.txt','r') as f:
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
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label.append(str(classes[class_ids[i]]))


            # confidence = str(round(confidences[i], 2))
            # color = colors[i]
            # cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
            # print(label)
            # cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (0, 255, 0), 2)
        insects = ', '.join(label)
    # import pdb;pdb.set_trace()
    return insects
# cv2.imshow('Image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
lbl = get_insects('https://60aa9fd223e7.ngrok.io/media/insects/%2B918130141308/a4bb5ff5-689f-46c5-aa65-b3d7a85b0ae9/images/1608274889.315205_AybEPk.jpeg')
print(lbl)