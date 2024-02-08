import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # backLegSensorValues = np.load("./data/back_leg_sensor_values.npy")
    # frontLegSensorValues = np.load("./data/front_leg_sensor_values.npy")
    front_motor_values = np.load("./data/front_leg_motor_angles.npy")
    back_motor_values = np.load("./data/back_leg_motor_angles.npy")
    # plt.plot(backLegSensorValues, label="Back Leg", linewidth=4)
    # plt.plot(frontLegSensorValues, label="Front Leg")
    plt.plot(front_motor_values, label="Front Leg", linewidth=4)
    plt.plot(back_motor_values, label="Back Leg",)
    plt.legend()
    plt.show()
