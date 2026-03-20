from power_temp_system import main as power_temp_system
from adcs_system import main as adcs_system
from camera_system import main as camera_system
from communication_system import send_data as downlink
import time
import datetime
import os
import shutil

print("\n\nALL SYSTEMS ONLINE\n")
DOWNLINK_DATA = "/home/sem/TrajectorySat/DOWNLINK_DATA"
images_path = "/home/sem/TrajectorySat/DOWNLINK_DATA/Images"
health_file = "/home/sem/TrajectorySat/DOWNLINK_DATA/health_status.txt"
adcs_file = "/home/sem/TrajectorySat/DOWNLINK_DATA/adcs.txt"

def check_directories():
    os.makedirs(DOWNLINK_DATA, exist_ok=True)
    os.makedirs(images_path, exist_ok=True)

def sleep_mode(duration = 60):
    global chg_request, health_file
    start_time = time.time()

    check_directories()

    while True:
        time.sleep(10)

        voltage, temperature = power_temp_system()

        if os.path.exists(health_file):
            with open(health_file, "a+") as status:
                status.write("{ts}|{volt}|{temp}\n".format(ts=time.time(), volt=voltage, temp=temperature))
        else:
            with open(health_file, "a+") as status:
                status.writelines(["TimeStamp|Voltage(V)|Temperature('C)\n", "{ts}|{volt}|{temp}\n".format(ts=time.time(), volt=voltage, temp=temperature)])

        if (time.time() - start_time) >= duration:
            return(True)

def science_mode(duration = 60):
    global images_path
    start_time = time.time()

    check_directories()

    while True:
        sleep_mode(1)
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

def downlink_mode():
    try:
        downlink(DOWNLINK_DATA)
        
        shutil.rmtree(DOWNLINK_DATA)

        os.mkdir(DOWNLINK_DATA)
        os.mkdir(images_path)
        os.remove("../DOWNLINK_DATA.zip")

        return(True)
    except Exception as e:
        return(e)