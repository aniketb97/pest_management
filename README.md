# Pest Pro - Pest Management Solution

[![License](https://img.shields.io/badge/License-Apache2-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0) [![Community](https://img.shields.io/badge/Join-Community-blue)](https://developer.ibm.com/callforcode/get-started/) [![Website](https://img.shields.io/badge/View-Website-blue)](https://sample-project.s3-web.us-east.cloud-object-storage.appdomain.cloud/)

Pests can be defined as insects or organisms that threaten crops. One of the major area of concern to handle during the growing phase of the crop is pest control and management. As pest impact crops growth, quality of the produce controlling and managing needs to be done with almost important. "Pest Pro" is an innovative way to identify and give sustainable solutions to manage these pests. 

## Contents

- [Pest Pro - Pest Management Solution](#pest-pro---pest-management-solution)
  - [Contents](#contents)
  - [Short description](#short-description)
    - [What's the problem?](#whats-the-problem)
    - [How can AI help?](#how-can-ai-help)
    - [Benefits](#benefits)
  - [Demo video](#demo-video)
  - [The architecture](#the-architecture)
  - [Long description](#long-description)
  - [Project roadmap](#project-roadmap)
  - [Getting started](#getting-started)
  - [Live demo](#live-demo)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Short description

### What's the problem?

**Heavy use of pesticides in farms** :\
Lack of knowledge about pests and sustainable practices to handle it.\
**Data Unavailability** :\
A central data source for all the pests currentlydoes not exist. There is a need for an image data bank of different types of pests.\
**Language Barrier** :\
Farmers need to be educated about pests in theircolloquial terms or local language.

### How can AI help?

Vision based pest identification and control solution enables identification of pest, region of infestation and probable pest control mechanism to be followed for the crop.

### Benefits

1. Quick and effective identification of pest.
2. Efficient application of pesticides there by reducing overall cost of produce. 
3. Improved Crop health and quality.
4. Avoiding side effects of pesticides on farmer/farm labors health. 


## Demo Video

[Demo Video available here.](./Demo_Video.mp4)

[Youtube link to demo video.](https://youtu.be/VuGPAZwr_D4). Please change resolution if video is distorted. (Recommended: 480p)

## The architecture

![Video transcription/translation app](https://github.com/aniketb97/pest_management/blob/main/Architecture.png)

1. All incoming message transactions will be track.
2. Will collect non-predicted images.
3. Will manually label images.
4. Move Labelled images to storage server.
5. Pull labelled images from GPU server.
6. Retrain model with newly labelled images.
7. Move model to model server for Prediction.


## Long description

[More detail is available here](./DESCRIPTION.md)

## Project roadmap

The project currently does the following things.

- Vision based AI model with 57 insects.
- WhatsApp channel to send photograph of pests to the server and get recommendations on their sustainable management.
- Application portal to add/modify recommendations for the identified pests, and get visual analysis of the user traffic.

See below for our proposed schedule on next steps after Call for Code 2021 submission.

![Roadmap](./roadmap.jpg)

## Live demo

You can find a running system to test at [this link](https://3.7.103.170/pestmanagement/).

## Authors

<a href="https://github.com/aniketb97/pest_management/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=aniketb97/pest_management" />
</a>

## License

This project is licensed under the Apache 2 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on [Billie Thompson's README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).