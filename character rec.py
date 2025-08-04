import cv2
import pytesseract
import os

# (Optional) Set path to tesseract executable if it's not in your system's PATH
# For Windows, uncomment and correct the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Check if image file exists
if not os.path.exists('8.png'):
    raise FileNotFoundError("The image file '8.png' was not found.")

# Load image
image = cv2.imread('8.png')

# Ensure image was loaded successfully
if image is None:
    raise ValueError("Failed to load the image. Check the path or file format.")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding (binary inverse)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Optional: Denoise or smooth the image
# thresh = cv2.medianBlur(thresh, 3)

# OCR using Tesseract with custom config
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(thresh, config=custom_config)

# Output the recognized text
print("Recognized Text:")
print(text)

# Show the thresholded image
cv2.imshow("Thresholded Image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()