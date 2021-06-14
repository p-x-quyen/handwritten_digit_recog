# Digit Recognition - GUI

## Demo
#### Predict

#### Visualize
https://user-images.githubusercontent.com/80868205/121943410-c08bf000-cd7b-11eb-94ac-d2bd3db21cfb.mp4

## Dataset
* MNIST

## Model
* Conv2D: 32 filters, size 3x3, Relu activation
* Conv2D: 64 filters, size 3x3, Relu activation
* MaxPooling2D: size 2x2
* Dropout: rate 0.25
* Dense: 256 units, Relu activation
* Dropout: rate 0.5
* Dense: 10 units, Softmax activation

## Accuracy
* 97.7% on test set

## Library
* tkinter
* PIL
* win32gui
* keras
* matplotlib
* numpy

## GUI
* Tkinter

## Run
1. Clone the project
2. Run file gui.py
