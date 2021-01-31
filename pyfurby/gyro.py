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

    def calculate_translation_matrix(self, vector):
        """
        One day I will write this.
        :return:
        """
        return vector

    @property
    def speed(self):
        """
        :return: how fast is it going? (velocity)
        """
        # technically multiplied by transformation matrix
        return self.calculate_translation_matrix(self.gyro.get_gyro_data())

    @property
    def acceleration(self):
        """
        :return: how fast is it speeding up? (acceleration)
        """
        # technically multiplied by transformation matrix
        return self.calculate_translation_matrix(self.gyro.get_accel_data())

    @property
    def temperature(self):
        """
        :return: temperature in Celcius
        """
        return self.gyro.get_temp()

    def is_lifted(self):
        """
        :return: true when lifted
        """
        return abs(self.speed['z']) > 10

    def is_moved(self):
        """
        :return: true when moved
        """
        return abs(self.speed['x']) > 10 or abs(self.speed['y']) > 10

    @property
    def lifted(self):
        """
        :return: lifted?
        """
        return self.is_lifted()

    @property
    def moved(self):
        """
        :return: moved?
        """
        return self.is_moved()

    def wait_until_moved(self):
        """
        Idle until moved
        """
        while not self.is_lifted() and not self.is_moved():
            pass




