import keras
from keras.models import Model
from keras.applications.mobilenetv2 import MobileNetV2
from keras.layers import *

def ChooseMultiLabel(input_shape = [224, 224, 3], 
                     dropout = 0.3,
                     classes = 1000,
                     trainable_layers = 5):

    base_model = MobileNetV2(weights = 'imagenet', include_top = False, input_shape = input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation = 'relu')(x)
    x = Dropout(dropout)(x)
    x = Dense(512, activation = 'relu')(x)
    x = Dropout(dropout)(x)
    outputs = Dense(classes, activation = 'sigmoid')(x)
    final_model = Model(inputs = base_model.input, 
                        outputs = outputs)
    
    for layer in final_model.layers:
        layer.trainable = True
        if isinstance(layer, BatchNormalization):
            layer.momentum = 0.8
    
    for layer in final_model.layers[:-trainable_layers]:
        layer.trainable = False
        
    return final_model