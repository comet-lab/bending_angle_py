class MovingAverageAngle:
    def __init__(self, window_size=5):
        """
        Initializes the MovingAverageAngle object.

        :param window_size: The size of the moving average window.
        """
        self.window_size = window_size
        self.values = []

    def add_angle(self, angle):
        """
        Adds an angle to the list of values and computes the moving average.

        :param angle: The angle to add.
        :return: The moving average of the last 'window_size' angles.
        """
        if len(self.values) >= self.window_size:
            self.values.pop(0)  # remove the oldest value if list is full
        self.values.append(angle)
        return self.compute_average()

    def compute_average(self):
        """
        Computes the average of the values.

        :return: The average of the values.
        """
        return sum(self.values) / len(self.values)
