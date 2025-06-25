import streamlit as st
import tensorflow as tf
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
import numpy as np

# Load your trained model ('super_final_alz.h5')
model = tf.keras.models.load_model('C:/jaaava/Final Year Project/Streamlit App/Streamlit App/valsplit20_epochs50_testacc98.h5')

# Function to make predictions on an image
def predict_image(model, img):
    # Preprocess the input image
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make predictions using the model
    predictions = model.predict(img_array)

    # Assuming you have a list of class labels for your model
    class_labels = ['Mild Demented', 'Moderate Demented', 'Non Demented', 'Very Mild Demented']  # Replace with your actual class labels

    # Map class indices to class labels
    decoded_predictions = [(class_labels[i], score) for i, score in enumerate(predictions[0])]

    # Sort predictions by confidence score
    decoded_predictions = sorted(decoded_predictions, key=lambda x: x[1], reverse=True)
    return decoded_predictions

# Streamlit app
st.title('Alzheimer\'s Detection')

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    img = image.load_img(uploaded_file, target_size=(176, 208))
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Make predictions if the 'Predict' button is clicked
    if st.button('Predict'):
        predictions = predict_image(model, img)
        st.write("Predictions:")
        for i, (label, score) in enumerate(predictions):
            st.write(f"{label}: {score:.2f}")