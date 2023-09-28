class LowPassFilter:
    def __init__(self, alpha=0.5):
        """
        Initializes the LowPassFilter object.

        :param alpha: The smoothing factor between 0 and 1. A smaller value means more smoothing.
        """
        self.alpha = alpha
        self.prev_value = None

    def add_angle(self, angle):
        """
        Adds an angle to the Low Pass Filter and computes the new value.

        :param angle: The angle to add.
        :return: The new filtered value of the angle.
        """
        if self.prev_value is None:
            self.prev_value = angle
        else:
            self.prev_value = self.prev_value + self.alpha * (angle - self.prev_value)
        return self.prev_value
