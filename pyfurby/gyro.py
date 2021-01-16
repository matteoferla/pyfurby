from mpu6050 import mpu6050

class FurbyGyro:
    """
    If the gyroscope were level, the re
    """
    resting_x = -5.547365246582031
    resting_y = -0.5051765502929687
    resting_z = -8.099584216308592

    def __init__(self):
        self.gyro = mpu6050(0x68)

    def define_static(self):
        """
        The furby is level and not moving, while earth gravity is still the same.
        The board is not z axis pointing to zenith, but at an angle
        :return:
        """
        acc = self.gyro.get_accel_data()
        self.resting_x = acc['x']
        self.resting_y = acc['y']
        self.resting_z = acc['z']

    def calculate_translation_matrix(self):
        pass

    def get_speed(self):
        # technically multiplied by transformation matrix
        return self.sensor.get_gyro_data()

    def get_acceleration(self):
        # technically multiplied by transformation matrix
        return self.sensor.get_accel_data()

    @property
    def temperature(self):
        return self.gyro.get_temp()

    def is_lifted(self):
        return abs(self.get_speed()['z']) > 10

    def is_moved(self):
        return abs(self.get_speed()['x']) > 10 or abs(self.get_speed()['y']) > 10

    @property
    def lifted(self):
        return self.is_lifted()

    @property
    def moved(self):
        return self.is_moved()

    def wait_until_moved(self):
        while not self.is_lifted() and not self.is_moved():
            pass




