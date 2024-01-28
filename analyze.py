import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    backLegSensorValues = np.load("./data/back_leg_sensor_values.npy")
    frontLegSensorValues = np.load("./data/front_leg_sensor_values.npy")
    plt.plot(backLegSensorValues, label="Back Leg", linewidth=4)
    plt.plot(frontLegSensorValues, label="Front Leg")
    plt.legend()
    plt.show()
