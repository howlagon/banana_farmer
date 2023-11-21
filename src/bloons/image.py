import pytesseract
import cv2
import pyscreeze
import numpy as np
from time import time

from PIL.Image import Image

def ocr(image: Image = None, bounds: list[int, int, int, int] = [0, 0, 1920, 1080], save: bool = False, threshold: tuple = (0, 255), invert: bool = False) -> str:
    assert image or bounds, "Either image or bounds must be provided."
    if image is None:
        image = pyscreeze.screenshot(region=tuple(bounds))
    if save:
        image.save(f"debug/preprocess-{time()}.png")
    array = np.array(image, dtype=np.uint8)
    _, array = cv2.threshold(array, threshold[0], threshold[1], cv2.THRESH_BINARY)
    if invert:
        array = cv2.bitwise_not(array)  
    image = cv2.cvtColor(array, cv2.COLOR_RGB2GRAY)
    if save:
        cv2.imwrite(f"debug/ocr-{time()}.png", image)
    text = pytesseract.image_to_string(image, config = "--psm 7")
    return text

def find_many_images(image_paths: list, original_image: None | Image = None, confidence: float = 0.9, return_coords: bool = False) -> int | tuple[int, list]:
    """Finds the first image in a list of images and returns the index. Can also return the position.

    Args:
        image_paths (list)
        original_image (None | Image, optional): _description_. Defaults to None.
        confidence (float, optional): Defaults to 0.9.

    Returns:
        int | tuple[int, list]: index | (index, [x, y, w, h])
    """
    if original_image is None:
        original_image = pyscreeze.screenshot()
    for index, image_path in enumerate(image_paths):
        try:
            located_image = pyscreeze.locate(image_path, original_image, confidence=confidence)
        except pyscreeze.ImageNotFoundException:
            continue
        if return_coords:
            return index, located_image
        return index
    return -1
    
def find_image(image_path: str, original_image: None | Image = None, confidence: float = 0.9) -> list | None:
    if original_image is None:
        original_image = pyscreeze.screenshot()
    try:
        located_image = pyscreeze.locate(image_path, original_image, confidence=confidence)
    except pyscreeze.ImageNotFoundException:
        return None
    return located_image

def get_pixel(image: Image, position: tuple[int, int]) -> tuple[int, int, int]:
    """Gets the pixel at a certain position in an image

    Args:
        image (Image)
        position (tuple[int, int])

    Returns:
        tuple[int, int, int]: (r, g, b)
    """
    return image.getpixel(position)

def screenshot(bounds: list[int, int, int, int] = [0, 0, 1920, 1080]) -> Image:
    screenshot = pyscreeze.screenshot(region=tuple(bounds))
    return screenshot