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


def genai_image(file_path, option1, option2):
    global uploaded_image
    folder_path = 'uploads/'
    # List all files in the folder
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.endswith(('jpg', 'jpeg', 'png', 'bmp', 'tiff', 'JPG'))]
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)
        uploaded_image = image_file
    color_name, hex_code = get_main_color_name_and_hex(uploaded_image)
    print(hex_code)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Given the hex value {hex_code}, identify the color name/"
                                      f"describe how it can be styled for {option1} outfits/"
                                      f"suggest how this color {option2} can paired with/"
                                      f"including all outfits option, offer recommendations on"
                                      f"how this color can be incorporated into with additional tips for makeup and "
                                      f"jewelry/"
                                      f"Provide insights into complementary and contrasting colors to enhance the "
                                      f"overall look.")
    return response.text


'''
def genai_text(query):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return response.text
'''

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: api_tester_code2.py /uploads")
        sys.exit(1)

    file_path = sys.argv[1]
    option1 = sys.argv[2]
    option2 = sys.argv[3]
    result = genai_image(file_path, option1, option2)
    print(result)
