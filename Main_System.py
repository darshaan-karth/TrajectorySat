from ADCS_System import main as adcs_system
from Camera_System import main as camera_system
import time
import datetime
import os
import shutil

print("\n\nALL SYSTEMS ONLINE\n")
adcs_file = "/home/sem/TrajectorySat/ADCS_Data/ADCS_Status.txt"
images_path = "/home/sem/TrajectorySat/Images"

def flatsat_mode(duration = 30):
    global images_path
    start_time = time.time()

    while True:
        time.sleep(10)  # Delay between iterations
        current = time.time()
        camera_system(FOLDER_PATH = images_path, current_time = current)
        acceleration, gyro, magnetic = adcs_system()

        if os.path.exists(adcs_file):
            with open(adcs_file, "a+") as status:
                status.write("{ts}|{accel}|{gyro}|{mag}\n".format(ts=current, accel=acceleration, gyro=gyro, mag=magnetic))
        else:
            with open(adcs_file, "a+") as status:
                status.writelines(["TimeStamp|Acceleration(m/s^2)|Gyro(rad/s)|Magnetic(Gauss)\n", "{ts}|{accel}|{gyro}|{mag}\n".format(ts=current, accel=acceleration, gyro=gyro, mag=magnetic)])

        if (time.time() - start_time) >= duration:
            return(True)

if __name__ == '__main__':
    flatsat_mode()