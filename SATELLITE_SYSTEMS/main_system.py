from communication_system import uplink_data as uplink
import modes
import sys

def main():
    while True:
        mode, duration = uplink()

        if mode == "DEORBIT":
            sys.exit(0)

        elif mode == "SLEEP":
            modes.sleep_mode(duration)

        elif mode == "SCIENCE":
            modes.science_mode(duration)

        elif mode == "COMMS":
            modes.downlink_mode()

if __name__ == "__main__":
    main()
