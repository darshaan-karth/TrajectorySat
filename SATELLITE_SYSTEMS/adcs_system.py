import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

def measure_imu(accel_gyro, mag):
    acceleration = accel_gyro.acceleration
    gyro = accel_gyro.gyro
    magnetic = mag.magnetic

    return(acceleration, gyro, magnetic)

def main():
    i2c = board.I2C()
    accel_gyro = LSM6DS(i2c)
    mag = LIS3MDL(i2c)
    
    acceleration, gyro, magnetic = measure_imu(accel_gyro, mag)
    return(acceleration, gyro, magnetic)

if __name__ == '__main__':
    main()
