import comms_system
import analysis_system
import time

modes = ["SLEEP", "SCIENCE", "COMMS", "DEORBIT", "ANALYZE"]

print("""
+========================+
| SELECT SATELLITE MODES |
+========================+
|    MODES   |   NUMBER  |
+========================+
|    SLEEP   |     0     |
|   SCIENCE  |     1     |
|    COMMS   |     2     |
|   DEORBIT  |     3     |
|   ANALYZE  |     4     |
+========================+""")
print("="*53)

while True:
    mode_request = int(input("Enter Mode Number: "))
    mode = modes[mode_request]
    
    if mode == "ANALYZE":
        analysis_system.analyze_data()
    elif mode == "DEORBIT":
        print("Sent request to change to {} mode".format(mode))
        comms_system.send_mode_data(mode, 0)
        print("="*53)
        break
    elif mode == "COMMS":
        print("Sent request to change to {} mode".format(mode))
        comms_system.send_mode_data(mode, 0)
        time.sleep(10)
        comms_system.recieve_data()
    else:
        duration = int(input("Duration of the Mode (Seconds): "))

        print("Sent request to change to {} mode for {} seconds".format(mode, duration))
        comms_system.send_mode_data(mode, duration)
        time.sleep(duration)

    print("="*53)