import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers.experimental.preprocessing import Rescaling
from tensorflow.keras import optimizers
from tensorflow.keras import regularizers


class Prediction_Model:

	CONST = {'IMG_HEIGHT' : 256,
	         'IMG_WIDTH'  : 256}

	CLASS_LABELS = {0 : 'Apple',
	                1 : 'Avocado',
	                2 : 'Banana',
	                3 : 'BeanSprout',
	                4 : 'Broccoli',
	                5 : 'Chicken',
	                6 : 'GreenBean',
	                7 : 'Potato',
	                8 : 'Salmon',
	                9 : 'Tomato'}

	learning_rate = 0.0005
	optmz       = optimizers.RMSprop(lr=learning_rate)
	num_classes = 10

	def __init__(self):
		Prediction_Model.pred_model = Prediction_Model.createModel()


	def createModel():
	    
	    xin = Input(shape=(256,256,3))
	    x = Rescaling(1./255) (xin)
	    
	    x = Conv2D(64,(3,3),activation=None, padding='same')(x)
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)

	    x = Conv2D(32,(3,3),activation=None, padding='same')(x)
	    x = BatchNormalization() (x)
	    x = Activation('relu') (x)
	    
	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(32,(3,3),activation=None, padding='same')(x)    
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(64,(3,3),activation=None, padding='same', kernel_regularizer=regularizers.l2(0.001))(x)
	    x = BatchNormalization() (x)   
	    x = Activation('relu') (x)
	    
	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Conv2D(128,(3,3),activation=None, padding='same', kernel_regularizer=regularizers.l2(0.001))(x)    
	    x = BatchNormalization() (x)       
	    x = Activation('relu') (x)

	    x = MaxPooling2D(pool_size=(2,2)) (x)
	    x = Flatten() (x)
	    x = Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)) (x)
	    x = Dropout(0.5) (x)
	    x = Dense(Prediction_Model.num_classes, activation='softmax') (x)


	    pred_model = Model(inputs=xin,outputs=x)
	    pred_model.compile(loss='categorical_crossentropy', 
	                  optimizer=Prediction_Model.optmz, 
	                  metrics=['categorical_accuracy'])

	    return pred_model


	def predict_image(self, image_path):
	    
	    PIL_img = load_img(
	        image_path,
	        color_mode = 'rgb',
	        target_size = (Prediction_Model.CONST['IMG_HEIGHT'], Prediction_Model.CONST['IMG_WIDTH']))
	    
	    ARR_img = img_to_array(PIL_img)
	    ARR_img = np.expand_dims(ARR_img, axis=0)
	    
	    Prediction_Model.pred_model.load_weights(modelpath)
	    Prediction_Model.pred_model.compile(loss='categorical_crossentropy',
	        optimizer=Prediction_Model.optmz,
	        metrics=['categorical_accuracy'])


	    predicts    = Prediction_Model.pred_model.predict(ARR_img)
	    predout     = Prediction_Model.CLASS_LABELS[int(np.argmax(predicts, axis=1))]
	    
	    return predout



if __name__ == "__main__":
	import os, pathlib
	folderpath = os.path.abspath(os.getcwd())
	model_folderpath = os.path.join(folderpath, 'model')
	prediction_folderpath = os.path.join(folderpath, 'pred_to_be_made')

	modelname = 'Food_Classification_Gen10'                                           #Model Name to be loaded
	modelpath = os.path.join(model_folderpath, modelname+'.hdf5')                     #Model Path to be loaded
	print(f"Model Path is: {modelpath}")

	image_path = os.path.join(prediction_folderpath, 'telegram_image1.jpg')           #Image Path to be predicted
	print(f"Image Path is: {image_path}")



	#Step 1: Initalise Prediction_Model Class
	Pred_Model = Prediction_Model()
	#Step 2: predict_image by passing in image_path of the image
	prediction = Pred_Model.predict_image(image_path)
	print(prediction)