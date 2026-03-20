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
MAX_RETRIES = 100
RETRY_INTERVAL = 2  # in seconds

def zip_folder(folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create the complete filepath of each file
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

def send_data(file_path):
    global satellite_address_global, GC_address_global

    try:
        # Create a Bluetooth socket using RFCOMM protocol
        downlink_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        downlink_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        downlink_socket.bind(satellite_address_global)

        # Listen for incoming connections and then connect
        downlink_socket.listen(1)
        uplink_socket = downlink_socket.accept()[0]
        
        # Open the image file in binary mode and send it in chunks
        try:
            zip_file_path = file_path+".zip"
            zip_folder(file_path, zip_file_path)

            data = uplink_socket.recv(1024).decode()
            if data == "FOLDER":
                uplink_socket.send(str(zip_file_path.split("/")[-1]).encode())
            else:
                sys.exit(0)

            with open(zip_file_path, "rb") as f:
                while (chunk := f.read(1024)):  # Read the image file in chunks of 1024 bytes
                    uplink_socket.send(chunk)
                    
        except Exception as e:
            print(f"Error sending data: {e}")
        finally:
            downlink_socket.close()
            uplink_socket.close()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def uplink_data():
    global satellite_address_global, GC_address_global
    
    retries = 0
    print("\nWaiting for Client Connection")
    while retries < MAX_RETRIES:
        try:
            # Create a Bluetooth socket using RFCOMM protocol and listen
            uplink_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            uplink_socket.connect(GC_address_global)  # Binding the server address
            print("SUCCESSFULLY CONNECTED")
            # Receive the mode change
            modes = ["SLEEP", "SCIENCE", "COMMS", "DEORBIT"]
            mode, duration = uplink_socket.recv(1024).decode().strip().split(";")
            duration = int(duration)

            if mode in modes:
                uplink_socket.send("OK_SAT".encode())
                print("Successfully Initiated {} mode for {} seconds".format(mode, duration))
                return(mode, duration)
            else:
                uplink_socket.send("NO MODE FOUND".encode())
                sys.exit(0)
            break

        except Exception as e:
            retries += 1
            if retries < MAX_RETRIES:
                time.sleep(RETRY_INTERVAL)
            else:
                print("Max retries reached. Unable to receive data.")
                sys.exit(0)

        finally:
            uplink_socket.close()

def main():
    #send_data("/home/sem/TrajectorySat/DOWNLINK_DATA/Images")
    #print(recieve_data())
    print("DONE")

if __name__ == "__main__":
    main()