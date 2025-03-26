import streamlit as st
from PIL import Image
import io
from inference_sdk import InferenceHTTPClient
import os

# --------------------------- #
# 🌍 ROBOFLOW INFERENCE CONFIG #
# --------------------------- #

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="Kp1AqMurWRBXStFinPNM"
)

MODEL_ID = "waste-management-ivrbu/1"  # Model ID and version
MIN_CONFIDENCE = 0.2  # Set confidence threshold to 40%


def waste_segregation():
    """Waste Segregation using Roboflow Inference SDK"""
    
    st.title("♻️ Waste Segregation Module")
    st.markdown("Upload an image of waste to classify it into categories")

    # Upload Image
    uploaded_file = st.file_uploader("Upload Waste Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to bytes
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="JPEG")
        image_bytes = image_bytes.getvalue()

        # Save image temporarily for inference
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(image_bytes)

        # Perform inference using Roboflow SDK
        with st.spinner("Classifying... 🔥"):
            try:
                result = CLIENT.infer(temp_image_path, model_id=MODEL_ID)

                # Parse and filter predictions
                predictions = result.get("predictions", [])
                filtered_predictions = [pred for pred in predictions if pred.get("confidence", 0) >= MIN_CONFIDENCE]

                if filtered_predictions:
                    for idx, pred in enumerate(filtered_predictions):
                        class_name = pred.get("class", "Unknown")
                        confidence = pred.get("confidence", 0) * 100

                        st.subheader(f"Prediction {idx + 1}: {class_name}")
                        st.info(f"Confidence: {confidence:.2f}%")

                        # Recycling guidelines
                        guidelines = {
                            "Organic": "Compost or use as fertilizer.",
                            "Plastic": "Recycle at a plastic waste facility.",
                            "Metal": "Send to a scrap metal collection center.",
                            "Paper": "Recycle in paper mills.",
                            "E-waste": "Dispose at authorized e-waste centers.",
                            "Glass": "Recycle at glass recycling facilities."
                        }

                        if class_name in guidelines:
                            st.write(f"**Recycling Tip:** {guidelines[class_name]}")
                        else:
                            st.warning("No recycling tip available for this category.")
                else:
                    st.warning("No high-confidence waste detected.")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Clean up temporary image
        os.remove(temp_image_path)
