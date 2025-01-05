import os
import time
import logging
from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
detection_batch_size = 30
recognition_batch_size = 30
langs = ["en"]  # Supported languages
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if not torch.cuda.is_available():
    logger.error("GPU not available, stopping program")
    exit()

# Model variables (lazy-loaded)
det_processor, det_model, rec_model, rec_processor = None, None, None, None

def load_models_once():
    """
    Lazily load the models and ensure they are loaded only once.
    """
    global det_processor, det_model, rec_model, rec_processor
    if not all([det_processor, det_model, rec_model, rec_processor]):
        logger.info("Loading models...")
        det_processor, det_model = load_det_processor(), load_det_model()
        rec_model, rec_processor = load_rec_model(), load_rec_processor()
        
        # Move models to appropriate device (CPU or GPU)
        det_model.to(device)
        rec_model.to(device)
        logger.info("Models loaded successfully.")

def process_image(image, langs, det_model, det_processor, rec_model, rec_processor):
    """
    Run OCR on the provided image.
    """
    predictions = run_ocr(
        [image],
        [langs],
        det_model,
        det_processor,
        rec_model,
        rec_processor,
        detection_batch_size=detection_batch_size,
        recognition_batch_size=recognition_batch_size,
    )
    return predictions

def extract_text_from_image(file_path):
    """
    Extract text from an image file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        # Open and resize the image
        image = Image.open(file_path)
        image.thumbnail((1024, 1024), Image.LANCZOS)  # Use LANCZOS for high-quality downsizing
    except Exception as e:
        raise ValueError("Invalid image file.")
    
    # Load models
    load_models_once()

    # Perform OCR
    start_time = time.time()
    predictions = process_image(image, langs, det_model, det_processor, rec_model, rec_processor)
    execution_time = time.time() - start_time
    logger.info("Execution time: %.2f seconds", execution_time)

    # Extract text from predictions
    ans = " ".join([each.text for each in predictions[0].text_lines])

    logger.info("Extracted text:\n%s", ans)
    return {"extracted_text": ans, "execution_time": execution_time}

if __name__ == "__main__":
    sample_file_path = "/path/to/your/sample/image.jpg"
    result = extract_text_from_image(sample_file_path)
    print(result)