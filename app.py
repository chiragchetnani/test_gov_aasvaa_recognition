import streamlit as st
import requests
from PIL import Image
import io

API_BASE_URL = "https://recognition.justifyai.in/api/v1"

st.set_page_config(page_title="Crop Detection Tester", page_icon="🌾")

st.title("🌾 Crop Detection API Tester")

tab1, tab2 = st.tabs(["Detect Crop", "Health Check"])

with tab1:
    st.header("Test Crop Detection")

    uploaded_file = st.file_uploader(
        "Upload an image (wheat, barley, or mustard)",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded_file is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

        if st.button("Detect Crop", type="primary"):
            with col2:
                st.subheader("Results")
                with st.spinner("Analyzing image..."):
                    try:
                        files = {
                            "image": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type,
                            )
                        }
                        response = requests.post(f"{API_BASE_URL}/detect", files=files)

                        if response.status_code == 200:
                            data = response.json()

                            st.success("Analysis Complete!")

                            st.metric(
                                "Valid Detection",
                                "✅ Yes" if data.get("is_valid") else "❌ No",
                            )

                            if data.get("crop_detected"):
                                st.metric(
                                    "Crop Detected", data["crop_detected"].title()
                                )
                                st.metric(
                                    "Confidence", f"{data['confidence'] * 100:.1f}%"
                                )
                            else:
                                st.info("No valid crop detected")

                            if data.get("raw_text"):
                                with st.expander("Raw API Response"):
                                    st.text(data["raw_text"])

                        elif response.status_code == 413:
                            st.error("Image too large")
                        elif response.status_code == 400:
                            st.error("Invalid file type")
                        else:
                            st.error(f"Error: {response.status_code}")

                    except requests.exceptions.ConnectionError:
                        st.error(
                            "Cannot connect to API. Make sure the server is running on port 8000"
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

with tab2:
    st.header("Health Check")

    if st.button("Check Health"):
        with st.spinner("Checking API health..."):
            try:
                response = requests.get(f"{API_BASE_URL}/health")

                if response.status_code == 200:
                    data = response.json()
                    st.success("API is healthy!")
                    st.json(data)
                else:
                    st.error(f"Health check failed: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to API. Make sure the server is running on port 8000"
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown(
    "**To run the API:** `cd /Users/chiragchetnani/app && source venv/bin/activate && python main.py`"
)
st.markdown("**To run Streamlit:** `streamlit run test_app.py`")
