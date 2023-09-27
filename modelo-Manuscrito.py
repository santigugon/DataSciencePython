# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 16:42:03 2022

@author: santi
"""
from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, ImageOps
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn import model_selection
from sklearn.linear_model import LinearRegression

import pandas as pd

import tensorflow
import keras #Se usa la libreria keras por su facil curva de aprendizaje y por la posibilidad que nos aporta de poder usar usando librerias del tipo backend como lo son TensorFlow, Theano o CNTK
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data() #En esta parte estamos cargando la base de datos, aprox. 60,000 imagenes de aprendizaje y unas 10,000 imagenes de testeo
print(x_train.shape, y_train.shape)

batch_size = 128
num_classes = 100
epochs = 10


x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
input_shape = (28, 28, 1)
# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu')) #Rectified linear activation function, will only output directly if it is positive otherwise outputs -
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy,optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])

#Aqui aplicamos el optimizador ADADELTA
#Esto arregla el problema de caida en tasa de aprendizaje y su necesidad de elegir una manualmente


hist = model.fit(x_train, y_train,batch_size=batch_size,epochs=epochs,verbose=1,validation_data=(x_test, y_test))
print("The model has successfully trained")
model.save('mnist.h5')
print("Saving the model as mnist.h5")


#Metricas de precision

#FP = confusion_matrix.sum(axis=0) - np.diag(confusion_matrix)  
#FN = confusion_matrix.sum(axis=1) - np.diag(confusion_matrix)
#TP = np.diag(confusion_matrix)
#TN = confusion_matrix.values.sum() - (FP + FN + TP)

# Sensitivity, hit rate, recall, or true positive rate
#TPR = TP/(TP+FN)
# Specificity or true negative rate
#TNR = TN/(TN+FP) 
# Precision or positive predictive value
#PPV = TP/(TP+FP)
# Negative predictive value
#NPV = TN/(TN+FN)
# Fall out or false positive rate
#FPR = FP/(FP+TN)
# False negative rate
#FNR = FN/(TP+FN)
# False discovery rate
#FDR = FP/(TP+FP)

# Overall accuracy
#ACC = (TP+TN)/(TP+FP+FN+TN)




#Mean squared error


import numpy as np
  
# Given values
Y_true = [1,1,2,2,4]  # Y_true = Y (original values)
  
# Calculated values
Y_pred = [0.6,1.29,1.99,2.69,3.4]  # Y_pred = Y'
  
# Mean Squared Error
prueba=slice(10000)
MSE = np.square(np.subtract(x_train[prueba],x_test)).mean()



#accuracy = metrics.accuracy_score(y_test, preds)
score = model.evaluate(x_test, y_test, verbose=0) #Verbose es la cantidad de detalle presentada por
#La computadora
print('Test loss:', score[0])
print('Test accuracy:', score[1])




model = load_model('mnist.h5')
def predict_digit(img):
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    img = img.convert('L')
    img=ImageOps.invert(img);
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        # Creating elements
        self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text = "Recognise", command =         self.classify_handwriting) 
        self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
        # Grid structure
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1,pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)
        #self.canvas.bind("<Motion>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)
    def clear_all(self):
        self.canvas.delete("all")
    def classify_handwriting(self):
        HWND = self.canvas.winfo_id() # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
        a,b,c,d=rect
        rect=(a+4,b+4,c+100,d+100)
        im = ImageGrab.grab(rect)
        digit, acc = predict_digit(im)
        self.label.configure(text= str(digit)+', '+ str(int(acc*100))+'%')
    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r=8
        self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')
app = App()
mainloop()



