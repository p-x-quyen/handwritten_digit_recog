# Digit Recognition - GUI

## Demo
#### Predict

#### Visualize
![visualize](https://user-images.githubusercontent.com/80868205/121943965-5293f880-cd7c-11eb-8931-584cdea8b0fc.gif)

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
