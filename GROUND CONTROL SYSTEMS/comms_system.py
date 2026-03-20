import socket
import zipfile
import os
import sys
import time

#GLOBAL CONSTANTS
satellite_address_global = ("D8:3A:DD:3B:FB:65", 4)
GC_address_global = ("A4:C3:F0:A4:12:CA", 4)

# Flag to control program termination
terminate_program = False
MAX_RETRIES = 10
RETRY_INTERVAL = 1  # in seconds

def unzip_folder(zip_file_path, extract_to_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)

def send_mode_data(mode, duration):
    global satellite_address_global, GC_address_global

    # Create a Bluetooth socket using RFCOMM protocol
    try:
        uplink_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        uplink_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        uplink_socket.bind(GC_address_global)

        # Listen for incoming connections and then connect
        uplink_socket.listen(1)
        downlink_socket = uplink_socket.accept()[0]
        
        # Open the image file in binary mode and send it in chunks
        try:
            text = "{};{}".format(mode, duration)
            downlink_socket.send(text.encode())
            conf_data = uplink_socket.recv(1024).decode()
            print(conf_data)

            if conf_data == "OK_SAT":
                print("Successfully Sent Mode Change")
            elif conf_data == "NO MODE FOUND":
                print("Satellite failed to recognize mode change request")
                sys.exit(0)
            else:
                print("Failed to send mode change request")
                sys.exit(0)
        finally:
            downlink_socket.close()
            uplink_socket.close()

    except Exception as e:
        print(f"Request Recieved & Changed by the TrajectorySAT")

def recieve_data():
    global satellite_address_global, GC_address_global, terminate_program
    retries = 0

    while retries < MAX_RETRIES:
        try:
            print("Trying to connect to satellite...")
            # Create a Bluetooth socket using RFCOMM protocol and Connect
            downlink_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            downlink_socket.connect(satellite_address_global)
            print(f"Connected to satellite")

            # Receive the file
            downlink_socket.send("FOLDER".encode())
            file_name = "../"+str(downlink_socket.recv(1024).decode()).strip()
            print(file_name)
            if file_name == "":
                print("ZIP File Not Found")
                sys.exit(0)

            with open(file_name, "wb") as f:
                while True:
                    if terminate_program:
                        print("Program terminated by user.")
                        sys.exit(0)
                    data = downlink_socket.recv(1024)  # Adjust the chunk size as necessary
                    if not data:
                        break
                    f.write(data)

            # Unzip the received file and clean up
            unzip_folder(file_name, file_name.replace(".zip", ""))
            os.remove(file_name)

            break  # Exit while loop if connection was successful and data was received

        except Exception as e:
            print(f"Error receiving data: {e}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying... Attempt {retries}/{MAX_RETRIES}")
                time.sleep(RETRY_INTERVAL)
            else:
                print("Max retries reached. Unable to connect to satellite.")
                sys.exit(0)
        
        finally:
            downlink_socket.close()