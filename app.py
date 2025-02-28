import os
import cv2
import torch
import subprocess
from pdf2image import convert_from_path
from PIL import Image

MODEL_PATH = "model.pt"  # Path to your trained model
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)

def process_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, img in enumerate(images):
        image_path = f"page_{i + 1}.jpg"
        img.save(image_path, "JPEG")
        image_paths.append(image_path)
    return image_paths

def detect_and_crop(model, image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detections = results.xyxy[0]

    if len(detections) == 0:
        return None, 0

    best_detection = max(detections, key=lambda x: x[4])
    xmin, ymin, xmax, ymax, confidence, _ = best_detection
    cropped = img[int(ymin):int(ymax), int(xmin):int(xmax)]
    cropped = cv2.resize(cropped, (600, 400))  # 6x4 format
    return cropped, confidence

def print_image(image_path):
    subprocess.run(f"lp {image_path}", shell=True)

def main(file_path):
    try:
        image_paths = process_pdf(file_path) if file_path.endswith('.pdf') else [file_path]
        best_cropped = None
        best_confidence = 0
        for image_path in image_paths:
            cropped, confidence = detect_and_crop(model, image_path)
            if cropped is not None and confidence > best_confidence:
                best_cropped = cropped
                best_confidence = confidence
        if best_cropped is not None:
            output_path = "cropped_label.jpg"
            cv2.imwrite(output_path, best_cropped)
            print_image(output_path)
            print(f"Label printed from: {file_path}")
        else:
            print("No label detected.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide an input file.")