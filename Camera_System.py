from picamera2 import Picamera2
import time

#PiCamera preview configuration
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
picam2.start()

def img_gen(FOLDER_PATH, current_time):
    """
    This function generates a new image name.

    Parameters:
        img_location (str): location of the image taken.
    """
    imgname = (f'{FOLDER_PATH}/image_{current_time}.jpg')
    return(imgname)

def take_photo(FOLDER_PATH, current_time, picam2):
    """
    This function takes a photo when the FlatSat is shaken.
    """
    #Capturing the image and saving it in the path stated in ADD_PATH
    ADD_PATH = img_gen(FOLDER_PATH, current_time)
    picam2.capture_file(ADD_PATH)
    print(f"Image captured and saved at {ADD_PATH}")
    return(ADD_PATH)

def main(FOLDER_PATH, current_time, push = False):  
    REPO_PATH = "/Images_Repository"

    img_path = take_photo(FOLDER_PATH, current_time, picam2)
    if (push):
        git_push(REPO_PATH=REPO_PATH, img_path=img_path)

if __name__ == '__main__':
    main()