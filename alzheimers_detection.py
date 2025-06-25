import streamlit as st
import test 
from test import predict_brain_tumor  
from chatbot import send_to_chatbot
from auth import log_scan_result

def app():
    st.header("🧠 Alzheimer's Detection System")

    try:
        uploaded_image = st.file_uploader("Upload an image for Alzheimer's Detection", type=["jpg", "png", "jpeg"])

        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

            if st.button("Detect Alzheimer's"):
                try:
                    encoded_label, decoded_label, confidence = predict_brain_tumor(uploaded_image)
                    confidence = float(confidence)

                    st.markdown(f"The image mainly belongs to the class **{decoded_label[0]}** with a confidence of **{confidence:.2f}%**.")
                    st.write("🔐 Current User:", st.session_state.get('username'))

                    if 'username' in st.session_state and st.session_state['username']:
                        log_scan_result(
                            st.session_state['username'],
                            "Alzheimer's Detection",
                            decoded_label[0],
                            confidence
                        )
                        st.success("✅ Scan logged to dashboard.")
                    else:
                        st.warning("⚠️ No user session found. Please log in before scanning.")

                    info = send_to_chatbot(f"Provide some info on the {decoded_label[0]} class for Alzheimer's.")
                    st.markdown("### ℹ️ Info about result:")
                    st.write(info)

                except Exception as e:
                    st.error(f"Prediction failed: {e}")

    except Exception as outer_error:
        st.error(f"Page failed to load: {outer_error}")
