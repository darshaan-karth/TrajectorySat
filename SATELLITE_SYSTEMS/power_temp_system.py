import subprocess

def power_stats():
    process = subprocess.Popen(['vcgencmd', 'measure_volts'], stdout=subprocess.PIPE)
    output, err = process.communicate()

    voltage = float(output.decode().strip().split("=")[1].replace("V", ""))
    return(voltage)

def temperature_stats():
    process = subprocess.Popen(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    output, err = process.communicate()

    temp = float(output.decode().split("=")[1].replace("'C", "").strip())
    return(temp)

def main():
    return(power_stats(), temperature_stats())

if (__name__ == "__main__"):
    main()