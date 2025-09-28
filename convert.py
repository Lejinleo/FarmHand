# Python script to convert a Hugging Face model to TFLite
from transformers import ViTForImageClassification, ViTImageProcessor
import tensorflow as tf
from PIL import Image
import numpy as np

# Load the model and processor from Hugging Face
model_name = "wambugu71/crop_leaf_diseases_vit"
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)

# Create a dummy input to trace the model
dummy_input = tf.convert_to_tensor(np.zeros((1, 224, 224, 3), dtype=np.float32))

# Convert the model to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the TFLite model
with open('crop_disease_model.tflite', 'wb') as f:
    f.write(tflite_model)