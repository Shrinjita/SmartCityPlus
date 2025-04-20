import streamlit as st
from PIL import Image
import io
from inference_sdk import InferenceHTTPClient
import os

# --------------------------- #
# 🌍 ROBOFLOW INFERENCE CONFIG #
# --------------------------- #

# Get API key from environment variables or Streamlit secrets
def get_roboflow_api_key():
    # First try to get from secrets
    if hasattr(st, 'secrets') and 'ROBOFLOW_API_KEY' in st.secrets:
        return st.secrets['ROBOFLOW_API_KEY']
    # Then try environment variables
    elif 'ROBOFLOW_API_KEY' in os.environ:
        return os.environ['ROBOFLOW_API_KEY']
    # Fallback for development only - REMOVE IN PRODUCTION
    else:
        st.warning("Using development API key. Set ROBOFLOW_API_KEY in environment variables or Streamlit secrets for production.")
        return "Kp1AqMurWRBXStFinPNM"  # This should be removed in production

@st.cache_resource
def get_inference_client():
    """Create and cache the inference client."""
    api_key = get_roboflow_api_key()
    return InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=api_key
    )

MODEL_ID = "waste-management-ivrbu/1"  # Model ID and version
MIN_CONFIDENCE = 0.4  # Increased confidence threshold to 40%


def waste_segregation():
    """Waste Segregation using Roboflow Inference SDK"""
    
    st.title("♻️ Waste Segregation Module")
    st.markdown("Upload an image of waste to classify it into categories")

    # Upload Image
    uploaded_file = st.file_uploader("Upload Waste Image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        try:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Convert image to bytes
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_bytes = image_bytes.getvalue()

            # Create a temp directory if it doesn't exist
            os.makedirs("temp", exist_ok=True)
            
            # Save image temporarily for inference
            temp_image_path = os.path.join("temp", "temp_image.jpg")
            with open(temp_image_path, "wb") as f:
                f.write(image_bytes)

            # Perform inference using Roboflow SDK
            with st.spinner("Classifying... 🔥"):
                try:
                    CLIENT = get_inference_client()
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
                        st.warning("No high-confidence waste detected. Try a clearer image or different angle.")
                
                except Exception as e:
                    st.error(f"Inference error: {e}")
                    st.info("Please try again with a different image or check your internet connection.")

            # Clean up temporary image
            try:
                os.remove(temp_image_path)
            except:
                pass  # Ignore errors in cleanup
                
        except Exception as e:
            st.error(f"Image processing error: {e}")
            st.info("Please try uploading a different image format.")