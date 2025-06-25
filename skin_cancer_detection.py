import streamlit as st
import test 
import numpy as np
from PIL import Image
from test import predict_skin_cancer
from chatbot import send_to_chatbot
from auth import log_scan_result

def app():
    st.header(" 🩺 Skin Cancer Detection")

    uploaded_image = st.file_uploader("Upload an image for Skin Cancer Detection", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        if st.button("Detect Skin Cancer"):
            predictions = predict_skin_cancer(img)
            class_names = ['Benign', 'Malignant']
            predicted_class_index = np.argmax(predictions)
            predicted_class = class_names[predicted_class_index]
            confidence = float(predictions[predicted_class_index] * 100)

            st.markdown(f"This image most likely belongs to the **{predicted_class}** class with a **{confidence:.2f}%** confidence.")
            st.write("🔐 Current User:", st.session_state.get('username'))

            if 'username' in st.session_state and st.session_state['username']:
                try:
                    log_scan_result(
                        st.session_state['username'],
                        "Skin Cancer Detection",
                        predicted_class,
                        confidence
                    )
                    st.success("✅ Scan logged to admin dashboard.")
                except Exception as e:
                    st.error(f"❌ Failed to log scan: {e}")
            else:
                st.warning("⚠️ No user session found. Please log in before scanning.")

            info = send_to_chatbot(f"Provide some info on the {predicted_class} class for Skin Cancer.")
            st.write(info)
