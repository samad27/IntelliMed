import streamlit as st
import numpy as np
import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageOps
import cv2
import io

# ---------------------------------------------------------------------------
# 🧠 Load all Models
brain_tumor_model = load_model('./brain_model3.h5')
lung_cancer_model = load_model('./LungCancer_model3.h5')
skin_cancer_model = load_model('./model_3.h5')
ecg_model = load_model('./ecgmodel.h5')

# Class Labels
brain_labels = ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary Tumor']
lung_labels = ['Benign', 'Malignant', 'Normal']
skin_labels = ['Benign', 'Malignant']
ecg_labels = {0: 'N', 1: 'S', 2: 'V', 3: 'F', 4: 'Q'}

# ---------------------------------------------------------------------------
# 🧹 Preprocessing Functions

def preprocess_mri_image(uploaded_file, target_size=(256, 256)):
    img = Image.open(uploaded_file).convert('RGB')   # ✅ Remove .read() and io.BytesIO
    img = ImageOps.crop(img, border=20)
    img = img.resize(target_size)
    img = np.array(img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    img = img.astype('float32') / 255.0
    return np.expand_dims(img, axis=0)


def preprocess_skin_image(image):
    img = image.resize((224, 224))
    img = np.array(img) / 255.0
    return np.expand_dims(img, axis=0)

def preprocess_lung_image(image):
    img = image.convert('L')
    img = img.resize((256, 256))
    img = np.array(img)
    img = np.expand_dims(img, axis=-1)
    img = img / 255.0
    return np.expand_dims(img, axis=0)

def preprocess_ecg(ecg_data):
    processed_data = ecg_data[:, :186]
    return processed_data.reshape(-1, 186, 1)

# ---------------------------------------------------------------------------
# 📈 Prediction Functions

def predict_brain_tumor(uploaded_image):
    img = preprocess_mri_image(uploaded_image)
    preds = brain_tumor_model.predict(img)
    decoded_label = brain_labels[np.argmax(preds)]
    confidence = np.max(preds) * 100
    return preds, decoded_label, confidence

def predict_lung_cancer(image):
    img = preprocess_lung_image(image)
    preds = lung_cancer_model.predict(img)
    predicted_class = lung_labels[np.argmax(preds)]
    confidence = np.max(preds) * 100
    return predicted_class, confidence

def predict_skin_cancer(image):
    img = preprocess_skin_image(image)
    preds = skin_cancer_model.predict(img)
    return preds[0]

def predict_ecg(ecg_data):
    data = preprocess_ecg(ecg_data)
    preds = ecg_model.predict(data)
    predicted_classes = [ecg_labels[np.argmax(pred)] for pred in preds]
    return predicted_classes

# ---------------------------------------------------------------------------
# 🧠 Blur Detection

def is_blurry(image_file, threshold=100.0):
    img = Image.open(io.BytesIO(image_file.read())).convert('L')
    img = np.array(img)
    variance_of_laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
    return variance_of_laplacian < threshold
