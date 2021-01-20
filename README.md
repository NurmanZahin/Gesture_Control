
[![LinkedIn][linkedin-shield]][linkedin-url]

# Gesture_Control
> An application to control your mouse using hand gestures and movements. Built using google mediapipe.

![](assets/vue_chatbot_demo.gif)

## Table of Contents
  - [Introduction](#introduction)
  - [Getting Started](#getting-started)
    - [Clone](#clone)
    - [Installing dependencies](#installing-dependencies)
  - [Usage](#usage)
  - [Gesture Controls](#gesture-controls)
  - [Acknowledgements](#acknowledgements)


## Introduction
This is an application using the hand pose estimation from [MediaPipe](https://github.com/google/mediapipe) to control your mouse. Simple mouse actions like holding the left button, double clicking and scrolling can be done using simple [gestures](#gesture-controls) as well.

## Getting Started

### Clone
- Cloning repo to your local setup
```shell
$ git clone https://github.com/NurmanZahin/Gesture_Control.git
```

### Installing dependencies
- Create a new conda environment
```shell
$ conda create --name gesture_control python=3.6.9
$ conda activate gesture_control
$ pip install -r requirements.txt
```

## Usage
- Try out the application, run the command below

```shell
$ cd src
$ python gesture_recognition.py
```
## Gesture Controls
| Mouse Action                                 | Gesture                                                                                                 |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Single Left Click                            | Put index finger and middle finger together. Putting them apart after this will release the left click. |
| Double Left Click                            | Put the index finger and thumb together.                                                                |
| Middle Mouse Button (For scrolling document) | Put the middle finger and thumb together.                                                               |
| Close Application                            | Put the thumb and pinky together.                                                                       |

## Acknowledgements 
- [MediaPipe](https://github.com/google/mediapipe)
- [Mouse controls](https://thecodacus.com/2017/08/16/gesture-recognition-virtual-mouse-using-opencv-python/)



[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: www.linkedin.com/in/nurman-jupri-20655814a
[product-screenshot]: images/screenshot.png