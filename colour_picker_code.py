import cv2
import numpy as np
from skimage import io
import webcolors


def extract_center_region(image, size=100):
    """
    Extract the central region of the image.

    Parameters:
    image (numpy array): The input image.
    size (int): The size of the central region to extract (size x size).

    Returns:
    numpy array: The central region of the image.
    """
    h, w, _ = image.shape
    center_x, center_y = w // 2, h // 2
    half_size = size // 2
    center_region = image[center_y - half_size:center_y + half_size, center_x - half_size:center_x + half_size]
    return center_region


def get_dominant_color(image):
    """
    Get the dominant color in an image using k-means clustering.

    Parameters:
    image (numpy array): The input image.

    Returns:
    Tuple: Dominant color in RGB format.
    """
    pixels = np.float32(image.reshape(-1, 3))
    n_colors = 1
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, _, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = palette[0]
    return dominant_color


def rgb_to_hex(rgb_color):
    """
    Convert RGB color to HEX code.

    Parameters:
    rgb_color (tuple): The RGB color.

    Returns:
    str: The HEX code.
    """
    return "#{:02x}{:02x}{:02x}".format(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))


def closest_color(requested_color):
    """
    Find the closest color name for the given RGB color.

    Parameters:
    requested_color (tuple): The RGB color.

    Returns:
    str: The closest color name.
    """
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def get_main_color_name_and_hex(image_path):
    """
    Analyze the image to get the main color name and HEX code of the central region.

    Parameters:
    image_path (str): The path to the image.

    Returns:
    Tuple: Main color name and its HEX code.
    """
    image = io.imread(image_path)
    center_region = extract_center_region(image)
    dominant_color = get_dominant_color(center_region)
    rgb_color = tuple(map(int, dominant_color))
    hex_color = rgb_to_hex(rgb_color)
    color_name = closest_color(rgb_color)

    return color_name, hex_color


# Example usage
if __name__ == "__main__":
    image_path = 'Screenshot_2024_0421_144530-1.jpg'  # Replace with your image path
    color_name, hex_code = get_main_color_name_and_hex(image_path)
    print(f"Main Color Name: {color_name}, HEX Code: {hex_code}")
