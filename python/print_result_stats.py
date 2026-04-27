import os
import json
import matplotlib
matplotlib.use('Agg')  # WAJIB untuk Docker

from matplotlib import pyplot as plt
from argparse import ArgumentParser
import numpy as np
import natsort 


def read_calib_json(file):
    with open(file, 'r') as f:
        results = json.load(f)
    return results
    

def main():
    parser = ArgumentParser("OpenICC")
    parser.add_argument('--path_results', 
                        default='', 
                        help="Path to calibration result JSON")
    args = parser.parse_args()

    # LOAD DATA
    data = read_calib_json(args.path_results)
    data = dict(data["trajectory"]) 
    data = natsort.natsorted(data.items())

    # EXTRACT PATH DATASET
    dataset_path = os.path.dirname(args.path_results)

    accl_spline = []
    accl_imu = []
    accl_bias = []
    gyro_spline = []
    gyro_imu = []
    gyro_bias = []
    t = []

    for d in data:
        t.append(d[0])
        accl_spline.append([d[1]["accl_spline"]["x"], d[1]["accl_spline"]["y"], d[1]["accl_spline"]["z"]])
        accl_imu.append([d[1]["accl_imu"]["x"], d[1]["accl_imu"]["y"], d[1]["accl_imu"]["z"]])
        accl_bias.append([d[1]["accl_bias"]["x"], d[1]["accl_bias"]["y"], d[1]["accl_bias"]["z"]])

        gyro_spline.append([d[1]["gyro_spline"]["x"], d[1]["gyro_spline"]["y"], d[1]["gyro_spline"]["z"]])
        gyro_imu.append([d[1]["gyro_imu"]["x"], d[1]["gyro_imu"]["y"], d[1]["gyro_imu"]["z"]])
        gyro_bias.append([d[1]["gyro_bias"]["x"], d[1]["gyro_bias"]["y"], d[1]["gyro_bias"]["z"]])

    # CONVERT KE NUMPY
    accl_spline_np = np.asarray(accl_spline)
    accl_imu_np = np.asarray(accl_imu)
    accl_bias_np = np.asarray(accl_bias)
    gyro_spline_np = np.asarray(gyro_spline)
    gyro_imu_np = np.asarray(gyro_imu)
    gyro_bias_np = np.asarray(gyro_bias)
    t_np = np.asarray(t)

    skip = 4

    # =========================
    # FIGURE 1
    # =========================
    fig1, ax = plt.subplots(2,1, figsize=(10,8))

    ax[0].set_title("Accelerometer - Spline vs IMU")
    ax[0].plot(accl_spline_np[0:-1:skip,0], 'r', label="spline x")
    ax[0].plot(accl_imu_np[0:-1:skip,0], 'r--', label="imu x")
    ax[0].plot(accl_spline_np[0:-1:skip,1], 'g', label="spline y")
    ax[0].plot(accl_imu_np[0:-1:skip,1], 'g--', label="imu y")
    ax[0].plot(accl_spline_np[0:-1:skip,2], 'b', label="spline z")
    ax[0].plot(accl_imu_np[0:-1:skip,2], 'b--', label="imu z")
    ax[0].set_xlabel("measurement")
    ax[0].set_ylabel("m/s2")
    ax[0].legend()

    ax[1].set_title("Gyroscope - Spline vs IMU")
    ax[1].plot(gyro_spline_np[0:-1:skip,0], 'r', label="spline x")
    ax[1].plot(gyro_imu_np[0:-1:skip,0], 'r--', label="imu x")
    ax[1].plot(gyro_spline_np[0:-1:skip,1], 'g', label="spline y")
    ax[1].plot(gyro_imu_np[0:-1:skip,1], 'g--', label="imu y")
    ax[1].plot(gyro_spline_np[0:-1:skip,2], 'b', label="spline z")
    ax[1].plot(gyro_imu_np[0:-1:skip,2], 'b--', label="imu z")
    ax[1].set_xlabel("measurement")
    ax[1].set_ylabel("rad/s")
    ax[1].legend()

    fig1.tight_layout()

    output1 = os.path.join(dataset_path, "plot_spline_vs_imu.png")
    plt.savefig(output1, dpi=300)
    plt.close()

    print(f"[INFO] Saved: {output1}")

    # =========================
    # FIGURE 2 (BIAS)
    # =========================
    fig2, ax = plt.subplots(2,1, figsize=(10,8))

    ax[0].set_title("Accelerometer bias")
    ax[0].plot(accl_bias_np[0:-1:skip,0], 'r', label="x")
    ax[0].plot(accl_bias_np[0:-1:skip,1], 'g', label="y")
    ax[0].plot(accl_bias_np[0:-1:skip,2], 'b', label="z")
    ax[0].set_xlabel("time")
    ax[0].set_ylabel("m/s2")
    ax[0].legend()

    ax[1].set_title("Gyroscope bias")
    ax[1].plot(gyro_bias_np[0:-1:skip,0], 'r', label="x")
    ax[1].plot(gyro_bias_np[0:-1:skip,1], 'g', label="y")
    ax[1].plot(gyro_bias_np[0:-1:skip,2], 'b', label="z")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("rad/s")
    ax[1].legend()

    fig2.tight_layout()

    output2 = os.path.join(dataset_path, "plot_bias.png")
    plt.savefig(output2, dpi=300)
    plt.close()

    print(f"[INFO] Saved: {output2}")


if __name__ == "__main__":
    main()
