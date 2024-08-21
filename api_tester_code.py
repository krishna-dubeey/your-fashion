import google.generativeai as genai
from colour_picker_code import get_main_color_name_and_hex
from dotenv import load_dotenv
import cv2
import os
import sys
import time

# Load environment variables from .env file
load_dotenv()
# Access the API key using os.environ
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def genai_image():
    folder_path = 'uploads/'
    # List all files in the folder
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.endswith(('jpg', 'jpeg', 'png', 'bmp', 'tiff'))]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)
        uploaded_image = image_file
    color_name,hex_code = get_main_color_name_and_hex(uploaded_image)
    print(hex_code )
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"What is this color {hex_code}? how can i pair this color shirt with pant")
    return response.text


def genai_text(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return response.text


if __name__ == '__main__':
    if len(sys.argv) > 1:
        query = sys.argv[1]
        results = genai_text(query)
        print(results)
    else:
        print("No query provided.")
    if len(sys.argv) > 1:
        file=genai_image()
        print(file)
