import streamlit as st
from test import predict_brain_tumor, is_blurry
from auth import log_scan_result
from chatbot import send_to_chatbot

def app():
    st.header('🧠 Brain Cancer Detection System')

    uploaded_image = st.file_uploader("Upload an MRI Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption='Uploaded Image', use_container_width=True)

        if st.button("Detect Brain Tumor"):
            if is_blurry(uploaded_image):
                st.error("Uploaded image is too blurry. Please upload a clearer MRI scan.")
            else:
                preds, decoded_label, confidence = predict_brain_tumor(uploaded_image)

                result_text = f"The image mainly belongs to the class **{decoded_label}** with a confidence of **{confidence:.2f}%**."
                st.markdown(result_text)

                current_user = st.session_state.get('username')
                st.write("🔐 Current User:", current_user)

                if current_user:
                    try:
                        log_scan_result(
                            username=current_user,
                            scan_type="Brain Tumor Detection",
                            result=decoded_label,
                            confidence=float(confidence)
                        )
                        st.success("✅ Scan logged to admin dashboard.")
                    except Exception as e:
                        st.error(f"❌ Failed to log scan: {e}")
                else:
                    st.warning("⚠️ No user session found. Please login.")

                info_prompt = f"Provide some info on the {decoded_label} class for Brain Tumor."
                info = send_to_chatbot(info_prompt)
                st.markdown("### ℹ️ Info about result:")
                st.write(info)
