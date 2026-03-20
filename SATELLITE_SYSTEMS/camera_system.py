from picamera2 import Picamera2
from PIL import Image
import time

#PiCamera preview configuration
picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

def img_gen(FOLDER_PATH, current_time):
    """
    This function generates a new image name.

    Parameters:
        img_location (str): location of the image taken.
    """
    imgname = (f'{FOLDER_PATH}/luna_{current_time}.jpg')
    return(imgname)

def take_photo(FOLDER_PATH, current_time, picam2):
    """
    This function takes a photo when the FlatSat is shaken.
    """
    # Capture image as a NumPy array
    picam2.start()
    image_array = picam2.capture_array()
    ADD_PATH = img_gen(FOLDER_PATH, current_time)

    # Convert NumPy array to PNG and save
    image = Image.fromarray(image_array)
    image.save(ADD_PATH)
    picam2.stop()

    print(f"Image captured and saved at {ADD_PATH}")
    return(ADD_PATH)

def main(FOLDER_PATH, current_time):  
    img_path = take_photo(FOLDER_PATH, current_time, picam2)

if __name__ == '__main__':
    main()
