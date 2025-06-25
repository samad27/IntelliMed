import streamlit as st
from PIL import Image
from test import predict_lung_cancer
from chatbot import send_to_chatbot
from auth import log_scan_result

def app():
    st.header(" 🫁 Lung Cancer Detection")

    uploaded_image = st.file_uploader("Upload an image for Lung Cancer Detection", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        st.image(img, caption="Uploaded Image", use_container_width=True)

        if st.button("Detect Lung Cancer"):
            predicted_class, confidence = predict_lung_cancer(img)
            confidence = float(confidence)

            st.markdown(f"The image mainly belongs to the **{predicted_class}** class with a confidence of **{confidence:.2f}%**.")
            st.write("🔐 Current User:", st.session_state.get('username'))

            if 'username' in st.session_state and st.session_state['username']:
                try:
                    log_scan_result(
                        st.session_state['username'],
                        "Lung Cancer Detection",
                        predicted_class,
                        confidence
                    )
                    st.success("✅ Scan logged to admin dashboard.")
                except Exception as e:
                    st.error(f"❌ Failed to log scan: {e}")
            else:
                st.warning("⚠️ No user session found. Please log in before scanning.")

            info = send_to_chatbot(f"Provide some info on the {predicted_class} class for Lung Cancer.")
            st.write(info)
