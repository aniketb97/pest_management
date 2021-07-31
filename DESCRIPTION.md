# Pest Pro - Pest Management Solution

One of the major area of concern to handle during the growing phase of the crop is pest control and management.
As pest impact crops growth, quality of the produce controlling and managing needs to be done with almost important.

To control pests and handle crops by providing right information to farmers through different channels/mediums. 
Our aim is to educate farmers by providing such information to handle problem statements.
Pest management provides such information to farmers through a WhatsApp channel.


## Scope

Pest Pro solution is comprised of 4 main parts:

#### Vision based AI model

The system has pre-trained vision based AI model to identify the pest to identify the pest from any photograph.
The same vision based AI model can be built with **Watson AI**, **visual-recognition-79** service.
This model is built using YOLO-v3.

#### WhatsApp channel

The system is configured with a WhatsApp channel to take image as input and provide a recommendation on pest control mechanisms.
Any farmer or individual user can use this channel to capture photograph of a pest, send it for identification and the said recommendation.

#### Application portal

The application portal provides features to add/modify recommendations for different pests. The portal also provides a dashboard that
shows vital information like transactions, pests indentified, unindentified/new pests, etc. Only a system administrator can access the
application portal. This portal can be deployed on **IBM Cloud Foundry**.

#### Build an image data bank

The system is collecting real time images directly from farmers through WhatsApp channel. Also, a system administrator can upload 
images of any pests into the portal. All these images stored in the storage server form a central image data bank. This centralised storage 
can be created on **IBM cloud storage** as well.

## Conclusion

Pest management has always been a very critical issue in the agriculture industry. Our solution presents a very simple yet innovative 
way to get sustainable and best practices to deal with pest related problems. Anyone with access to WhatsApp can benefit from this solution.

### Results

Currently, the system is trained with 57 pests and all 57 pest information is provided in portal as well. So, our solution can provide 
recommendation of the trained 57 pests. 

## Acknowledgments

Tech Mahindra MAKERS LAB Leadership:
1. Nikhil Malhotra
2. Kanchan Bhonde
