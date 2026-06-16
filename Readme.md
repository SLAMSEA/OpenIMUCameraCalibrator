# Breaking Changes

* **1/7/2024**:
  * Removed javascript requirement. Please install py_gpmf_parser from now on.
  * Fixed Dockerfile and updated Readme with new installation instructions
  * Updated dependencies to Ceres 2.1.0
  * Updated pyTheiaSfM version --> Install new version (either master or 69c3d37).

---

# OpenICC: An Open IMU and Camera Calibrator

I developed this repository to experiment with the accurate calibration of action cameras (e.g. GoPro cameras) to use them for geometric vision tasks like Structure-from-Motion, Photogrammetry and SLAM. Modern action cameras are equipped with various sensors like IMUs (accelerometer, gyroscope and magnetometer) and GPS. However the calibration data (e.g. camera projection and IMU to camera transformations) is not available.

This is where the OpenImuCameraCalibrator comes in. With this toolbox you can:

* Calibrate the intrinsics of your a GoPro camera. Supported **camera models** are:
  * Fisheye [6]
  * Division Undistortion [5]
  * Field-of-View [3]
  * Double Sphere [2]
  * Extended Unified [4]
  * Pinhole
  * Pinhole with radial-tangential distortion
* Extract the meta data integrated in the MP4 video file (called **telemetry data**)
* Calibrate the **Camera to IMU rotation matrix** and find the dataset dependent **time offset**
* Perform full **continuous time batch optimization** to find the full transformation matrix between IMU and camera
* Do an intrinsic calibration of your IMU using the method described in [11]
* [Experimental] Calibrate the **rolling shutter line delay** (not really working yet)

---

## Results

This section provides some results for my two GoPro cameras (6 and 9). You can use this to verify your own results or use them as initial values for your application. So far I have been setting them to FullHD with wide FoV and 30/60 fps. This is probably the most common setting that people use.

### Camera Calibration

| Dataset | Camera | Setting | Camera model | Intrinsics (f, cx, cy) | Reproj error |
|--|--|--|--|--|--|
| 1 | GoPro 9 | 960x540 / 60fps / Wide | Division Undistortion | (437.13, 489.07, 270.87) Dist: -1.4386e-06 | 0.31 |
| 2 | GoPro 9 | 960x540 / 60fps / Wide | Extended Unified | (437.97, 489.47, 272.02) Alpha: 0.5115 Beta: 1.062  | 0.209 |
| 3 | GoPro 9 | 960x540 / 60fps / Wide | Fisheye | (435.45, 479.12, 274.46) d1:0.05 d2:0.07 d3:-0.11 d4:0.05  | 0.24 |
| 4 | GoPro 6 | 960x540 / 60fps / Wide | Division Undistortion | (438.59, 480.80, 274.80) Dist: -1.47079-06  | 0.09 |
| 5 | GoPro 6 | 960x540 / 60fps / Wide | Double Sphere | (342.43, 472.60, 273.88) XI: -0.215 Alpha 0.5129 | 0.16 |
| 6 | GoPro 6 | 960x540 / 60fps / Wide | Fisheye | (439.13, 479.66, 273.19) d1: 0.046, d2: 0.064, d3:-0.10, d4: 0.052 | 0.17 |
| 7 | GoPro 6 | 960x540 / 30fps / Wide | Division Undistortion | (436.06, 481.87, 272.58) dist: -1.468e-6 | 0.16 |

### IMU to Camera Calibration

| Dataset | Time offset IMU to camera | dt_r3 / dt_so3 | T_camera_to_imu (qw,qx,qy,qz) (tx,ty,tz)_m | RS Line delay init / calib | Final mean reproj error |
|--|--|--|--|--|--|
| 1 | -0.0813s | 0.128/0.056 | (0.0048,-0.006,-0.7076,0.7065),(0.0069,-0.0217, 0.001) | 30.895 / 31.62 | 0.84 |
| 2 | -0.0813s | 0.072/0.048 | (0.005,-0.0068,-0.7083,0.7057),(0.0021, -0.018,-0.004) | 30.895 / 36.56 | 0.82 |
| 3 | -0.0815s | 0.089/0.050 | (0.0001,-0.0002,0.7100,-0.7040),(0.009,-0.0182,-0.001) | 30.895 / 33.38 | 0.83 |
| 4 | -0.0129s | 0.15/0.062 | (-0.005,0.003,-0.706,0.7080),(0.009, -0.019, 0.012) | 30.895 / 29.58 | 0.79 |
| 5 | -0.0127s | 0.060/0.051 | (0.0007,-0.007,0.705,-0.7085),(0.005,-0.017, 0.008) | 30.895 / 26.03 | 0.59 |
| 6 | -0.0127s | 0.15/0.054 | (0.006,-0.006,0.706,-0.7072),(0.007,-0.030, 0.010) | 30.895 / 28.33 | 0.66 |
| 7 | -0.0129s | 0.056/0.035 | (-0.002,-0.0026,0.7049,-0.7092),(0.0216,-0.0165, 0.0108) | 61.79 / 61.76 | 0.9 |

### Some SLAM Examples using ORB-SLAM3

* [GoPro9_25fps_1080](https://youtu.be/0wIqkUEjhiw)
* [GoPro9_50fps_1080](https://youtu.be/IOpty7u7_04)
* [GoPro9_25fps_1440_maxlens_fisheye](https://youtu.be/Phw_OVP6sxI)
* [ORB-SLAM3 fork](https://github.com/urbste/ORB_SLAM3/)

---

## Installation Instructions

Tested on Ubuntu 18.04, 20.04, and 22.04.

**1. Clone and build [OpenCV](https://github.com/opencv/opencv) >= 4.5.0** with [contrib](https://github.com/opencv/opencv_contrib) modules. Contrib modules are required for Aruco marker detection. On Ubuntu 22.04 you can also install directly from apt:

```bash
sudo apt-get install libopencv-dev libopencv-contrib-dev
```

**2. Install [Ceres 2.1](http://ceres-solver.org/installation.html)**

```bash
git clone https://github.com/ceres-solver/ceres-solver
git checkout 2.1.0
mkdir -p build && cd build && cmake .. -DBUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release
sudo make -j install
```

**3. Clone and build the [TheiaSfM fork](https://github.com/urbste/pyTheiaSfM)**

```bash
git clone https://github.com/urbste/pyTheiaSfM
cd pyTheiaSfM && git checkout 69c3d37 && mkdir -p build && cd build
cmake .. && make -j
sudo make install
```

**4. Build this project**

```bash
git clone https://github.com/urbste/OpenImuCameraCalibrator
mkdir -p build && cd build && cmake ..
make -j
```

**5. Create a Python >3.5 environment** (or use your local Python — not recommended)

```bash
pip install -r requirements.txt
```

---

## Docker

### Building and Running with Docker (Original Instructions)

Build the Docker container:

```bash
docker build -t openicc .
```

Mount the OpenICC folder and your calibration dataset into the container (e.g., after downloading the [GoPro9 dataset](https://drive.google.com/file/d/1XjtUX-4ZI0Ydkd2O3BWnaUzfmzm96He4/view?usp=share_link) to `/home/Downloads/GoPro9`):

```bash
docker run -it --rm -v `pwd`:/home -v /home/Downloads/GoPro9:/dataset openicc
```

Run the calibration inside the container:

```bash
cd /home
python3 python/run_gopro_calibration.py --path_calib_dataset /dataset/dataset3/ --path_to_build ../OpenImuCameraCalibrator/build/applications/
```

### Docker Installation on Ubuntu (SLAMSEA Procedure)

The following steps describe installing Docker on a fresh Ubuntu system for use with OpenICC in the SLAMSEA pipeline.

**Update system package lists:**

```bash
sudo apt update
```

**Install Docker:**

```bash
sudo apt install docker.io -y
```

**Enable and start the Docker service:**

```bash
sudo systemctl enable docker
sudo systemctl start docker
docker --version
```

After running these commands, the Docker version will be displayed in the terminal, confirming that the installation succeeded.

**Add the current user to the Docker group** (required to run Docker without `sudo`):

```bash
sudo usermod -aG docker $USER
```

> **Note:** Log out and back in (or run `newgrp docker`) for the group change to take effect.

---

## SLAMSEA Workflow

OpenICC is used within the [SLAMSEA](https://github.com/SLAMSEA) project as the primary calibration tool for monocular visual-inertial navigation systems. In this context, OpenICC is responsible for:

* **Camera calibration** — estimating intrinsic lens parameters
* **Camera–IMU calibration** — determining the 6-DOF spatial and temporal relationship between the camera and the IMU
* **IMU bias calibration** — characterising sensor noise via Allan Variance analysis
* **Visual-Inertial Navigation preparation** — producing calibrated parameters suitable for state estimators
* **ORB-SLAM3 configuration generation** — generating YAML configuration files for the ORB-SLAM3 visual-inertial SLAM system

The entire SLAMSEA calibration pipeline runs inside Docker, providing a reproducible, dependency-free processing environment that can be used consistently across different host machines.

### Recommended Directory Layout

The SLAMSEA project uses the following top-level directory structure:

```text
~/SLAMSEA/
├── software/         # Cloned repositories (OpenICC, ORB-SLAM3, etc.)
├── datasets/         # Raw video and telemetry data, organised by camera model
├── calibration/      # Calibration output files (imu_bias_calibration.txt, camera_imu_calibration.txt)
└── configs/          # ORB-SLAM3 YAML configuration files, organised by camera model
```

> **Recommendation:** Maintain this separation between software, data, calibration outputs, and configuration files to simplify reproducibility across multiple datasets and camera models.

### Setting Up the Project Folder

Navigate to the software directory and create the OpenICC working folder:

```bash
cd ~/SLAMSEA/software
mkdir -p OpenICC
cd OpenICC
```

Clone the SLAMSEA fork of OpenIMUCameraCalibrator:

```bash
git clone https://github.com/SLAMSEA/OpenIMUCameraCalibrator.git
cd OpenIMUCameraCalibrator
```

Build the Docker image:

```bash
docker build -t openicc .
```

> **Note:** The Docker build process installs all required dependencies automatically. Build time is typically 20–30 minutes depending on hardware.

---

## Dataset Structure

The SLAMSEA calibration pipeline expects calibration data to be organised within a dedicated subdirectory of the camera-specific dataset folder. The required structure is:

```text
~/SLAMSEA/datasets/<CameraModel>/
├── monocular_visual_inertial_calibration/
│   ├── cam/          # Camera intrinsics calibration video(s)
│   ├── cam_imu/      # Camera–IMU extrinsics calibration video(s)
│   └── imu_bias/     # IMU bias calibration video(s) for Allan Variance
└── trajectory_surveys/
    └── <survey_video>.MP4   # Navigation trajectory video(s)
```

**Directory purposes:**

| Directory | Purpose |
|---|---|
| `cam/` | Stores video(s) of an Aruco/AprilTag calibration board used to estimate camera intrinsic parameters. |
| `cam_imu/` | Stores video(s) of the calibration board recorded with simultaneous IMU data, used to estimate the 6-DOF camera–IMU transformation. |
| `imu_bias/` | Stores video(s) recorded with the camera stationary, providing IMU data for Allan Variance noise characterisation. |
| `trajectory_surveys/` | Stores navigation trajectory video(s) used for ORB-SLAM3 processing after calibration is complete. |

Create the calibration subdirectory structure as follows:

```bash
cd ~/SLAMSEA/datasets/<CameraModel>
mkdir -p monocular_visual_inertial_calibration/cam
mkdir -p monocular_visual_inertial_calibration/cam_imu
mkdir -p monocular_visual_inertial_calibration/imu_bias
```

Place calibration videos in the corresponding folders before running the Docker container.

### Launching Docker for Calibration

From the OpenIMUCameraCalibrator directory, launch the container and mount the camera dataset:

```bash
cd ~/SLAMSEA/software/OpenICC/OpenIMUCameraCalibrator

docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ~/SLAMSEA/datasets/<CameraModel>:/dataset \
  openicc
```

Verify that the dataset is accessible inside the container:

```bash
ls /dataset
```

The terminal should display `monocular_visual_inertial_calibration` and `trajectory_surveys`.

---

## Allan Variance Workflow (IMU Bias Calibration)

The Allan Variance method characterises the stochastic noise properties of the IMU sensors, producing the four noise parameters required by ORB-SLAM3 and other visual-inertial estimators.

### Step 1 — Extract Telemetry from IMU Bias Videos

Inside the Docker container, run the telemetry extraction script pointing to the `imu_bias` folder:

```bash
python3 python/merge_gopro_telemetry_from_folder.py \
  --path_calib_dataset \
  /dataset/monocular_visual_inertial_calibration/imu_bias
```

This script parses the GPMF telemetry streams embedded in each GoPro MP4 file and merges them into a single unified file. When processing is complete, the terminal displays `done`.

**Output files in `imu_bias/`:**

* Individual telemetry JSON files for each input video
* `merged_telemetry.json` — the combined telemetry file used in the next step

> **Note:** Using multiple stationary recordings (two or more videos) increases the total IMU data duration and improves Allan Variance estimate quality.

### Step 2 — Run Allan Variance Fitting

```bash
/home/build/applications/fit_allan_variance \
  --telemetry_json=/dataset/monocular_visual_inertial_calibration/imu_bias/merged_telemetry.json \
  2>&1 | tee /dataset/monocular_visual_inertial_calibration/logFitAllanVariance.txt
```

The output log `logFitAllanVariance.txt` is written to the `monocular_visual_inertial_calibration/` directory.

### Allan Variance Output Parameters

Results are reported per axis (X, Y, Z) for both accelerometer and gyroscope. Average the three axes for each parameter to obtain the four scalar values required for ORB-SLAM3:

| Parameter | Unit | ORB-SLAM3 field |
|---|---|---|
| Accelerometer White Noise | m/s²/√Hz | `IMU.NoiseAcc` |
| Accelerometer Bias Instability | m/s²·√Hz | `IMU.AccWalk` |
| Gyroscope White Noise | rad/s/√Hz | `IMU.NoiseGyro` |
| Gyroscope Bias Instability | rad/s·√Hz | `IMU.GyroWalk` |

**Parameter descriptions:**

* **Accelerometer White Noise** (`NoiseAcc`) — broadband measurement noise on the accelerometer, proportional to 1/√Hz. Determines position random walk in the integrated trajectory.
* **Accelerometer Bias Instability** (`AccWalk`) — slow, correlated drift of the accelerometer zero offset over time. Models the random walk of the bias term in the IMU pre-integration.
* **Gyroscope White Noise** (`NoiseGyro`) — broadband measurement noise on the gyroscope. Determines orientation random walk when the rate is integrated to attitude.
* **Gyroscope Bias Instability** (`GyroWalk`) — slow, correlated drift of the gyroscope zero offset over time. Critical for long-duration visual-inertial navigation.

Save the averaged results to a summary file for later use in ORB-SLAM3 configuration:

```
~/SLAMSEA/calibration/<CameraModel>/monocular_visual_inertial/imu_bias_calibration.txt
```

---

## Camera–IMU Calibration Workflow

After IMU bias characterisation, run the full camera–IMU calibration using the video(s) in `cam_imu/`.

> **Warning:** The calibration board used during recording must match the target configuration embedded in OpenICC. Using a different board without updating the target parameters will cause calibration failure.

Inside the Docker container, run:

```bash
python3 python/run_gopro_calibration.py \
  --path_calib_dataset /dataset/monocular_visual_inertial_calibration \
  --path_to_build /home/build/applications/ \
  2>&1 | tee /dataset/monocular_visual_inertial_calibration/logOpenICC.txt
```

Processing time is typically 10 minutes, depending on hardware.

### Camera–IMU Calibration Outputs

The calibration produces the following outputs:

| Output | Description |
|---|---|
| `logOpenICC.txt` | Full optimisation log containing the estimated rotation matrix and translation vector |
| `Plot Bias.png` | Visualisation of IMU sensor bias characteristics over time |
| `Plot Spline vs IMU.png` | Comparison of B-spline trajectory estimate against raw IMU measurements |
| Supporting files in `cam/`, `cam_imu/`, `imu_bias/` | Intermediate files from the optimisation pipeline |

### Key Estimated Parameters

**Rotation matrix (R):** A 3×3 matrix representing the orientation of the camera frame relative to the IMU frame. Extracted from the final optimisation result in `logOpenICC.txt`.

**Translation vector (t):** A 3-element vector `[tx, ty, tz]` representing the position of the camera origin in the IMU frame (in metres).

**Time offset:** A scalar (in seconds) representing the synchronisation lag between camera frame timestamps and IMU measurement timestamps.

These parameters together define the **camera-to-IMU extrinsic transformation**, which is assembled into the 4×4 homogeneous `Tbc` matrix for ORB-SLAM3.

Save the rotation matrix and translation vector to:

```
~/SLAMSEA/calibration/<CameraModel>/monocular_visual_inertial/camera_imu_calibration.txt
```

---

## ORB-SLAM3 Integration

OpenICC calibration outputs are combined with camera intrinsics to produce ORB-SLAM3 YAML configuration files. The following parameters are sourced directly from OpenICC:

### Tbc Matrix

The `Tbc` matrix encodes the 4×4 homogeneous transformation from the camera body frame to the IMU body frame, constructed from the rotation matrix and translation vector obtained from `logOpenICC.txt`:

```
Tbc: !!opencv-matrix
   rows: 4
   cols: 4
   dt: f
   data: [R00, R01, R02, tx,
           R10, R11, R12, ty,
           R20, R21, R22, tz,
           0.0, 0.0, 0.0, 1.0]
```

### IMU Noise Parameters

The four scalar values from Allan Variance are entered into the ORB-SLAM3 YAML as:

```yaml
IMU.NoiseGyro:  <gyroscope_white_noise>    # rad/s/√Hz
IMU.NoiseAcc:   <accelerometer_white_noise> # m/s²/√Hz
IMU.GyroWalk:   <gyroscope_bias_instability> # rad/s·√Hz
IMU.AccWalk:    <accelerometer_bias_instability> # m/s²·√Hz
IMU.Frequency:  <imu_sampling_rate>         # Hz
```

### Example ORB-SLAM3 YAML Configuration

The following is a complete example configuration file generated from the SLAMSEA GoPro HERO10 Black calibration. Substitute your own calibrated values as appropriate:

```yaml
%YAML:1.0

#--------------------------------------------------------------------------------------------
# Camera Parameters
#--------------------------------------------------------------------------------------------
Camera.type: "PinHole"

# Camera calibration and distortion parameters
# (OpenICC https://github.com/urbste/OpenImuCameraCalibrator)
Camera.fx: 1196.0800000000
Camera.fy: 1192.8700000000
Camera.cx: 949.2240000000
Camera.cy: 524.7240000000

Camera.k1: -0.0982107000
Camera.k2:  0.1096860000
Camera.p1:  0.0002478240
Camera.p2: -0.0004722020

# Camera resolution
Camera.width:  1920
Camera.height: 1080

# Camera frames per second
Camera.fps: 29.97

# Color order of the images (0: BGR, 1: RGB. Ignored if images are grayscale)
Camera.RGB: 1

# Transformation from camera to IMU (body frame)
# Calibrated with OpenICC https://github.com/urbste/OpenImuCameraCalibrator
Tbc: !!opencv-matrix
   rows: 4
   cols: 4
   dt: f
   data: [-0.9164710000, -0.3950490000,  0.0633826000,  0.0787929000,
           0.0093455300, -0.1795100000, -0.9837120000,  0.2070220000,
           0.3999920000, -0.9009510000,  0.1682070000,  0.1000260000,
           0.0,           0.0,           0.0,           1.0]

# IMU noise parameters
# Use OpenICC https://github.com/urbste/OpenImuCameraCalibrator
IMU.NoiseGyro: 0.0013514867   # rad/s/√Hz
IMU.NoiseAcc:  0.0137850667   # m/s²/√Hz
IMU.GyroWalk:  0.0000515426   # rad/s·√Hz
IMU.AccWalk:   0.0004464330   # m/s²·√Hz
IMU.Frequency: 200

#--------------------------------------------------------------------------------------------
# ORB Parameters
#--------------------------------------------------------------------------------------------
ORBextractor.nFeatures:   75000
ORBextractor.scaleFactor: 1.1
ORBextractor.nLevels:     20
ORBextractor.iniThFAST:   5
ORBextractor.minThFAST:   2

#--------------------------------------------------------------------------------------------
# Viewer Parameters
#--------------------------------------------------------------------------------------------
Viewer.KeyFrameSize:      0.05
Viewer.KeyFrameLineWidth: 1
Viewer.GraphLineWidth:    0.9
Viewer.PointSize:         2
Viewer.CameraSize:        0.08
Viewer.CameraLineWidth:   3
Viewer.ViewpointX:        0
Viewer.ViewpointY:        -0.7
Viewer.ViewpointZ:        -3.5
Viewer.ViewpointF:        500
```

Save this file as:

```
~/SLAMSEA/configs/<CameraModel>/monocular_visual_inertial.yaml
```

> **Recommendation:** Keeping YAML configuration files separate from the ORB-SLAM3 source tree allows the same calibration to be reused across multiple survey datasets without modifying the repository.

### Trajectory Telemetry Extraction

After completing calibration, extract IMU telemetry from the navigation trajectory video for use in ORB-SLAM3 processing. Inside the Docker container:

```bash
cd javascript

node extract_metadata.js \
  /dataset/trajectory_surveys \
  <trajectory_video_filename>.MP4 \
  /dataset/trajectory_surveys
```

When extraction is complete, the terminal displays `Done`. The output telemetry file is written to the `trajectory_surveys/` folder and contains the IMU sensor data recorded during the navigation survey.

Exit the Docker container when all processing is complete:

```bash
exit
```

---

## Usage Examples

* [Calibrate a GoPro9](docs/gopro_calibration.md)
* [Calibrate a SamsungS20FE](docs/samsung_s20_calibration.md)
* [Calibrate a GoPro IMU intrinsics](docs/imu_intrinsics.md)
* [Estimate a GoPro IMU noise parameters](docs/imu_noise_parameters.md)

---

## Acknowledgements

This library would not have been possible without these great open-source projects:

* [TheiaSfM](http://theia-sfm.org) — Camera models and optimization
* [Basalt-Headers]() — Spline implementation and optimization
* [Lie Group Cumulative B-Splines](https://gitlab.com/tum-vision/lie-spline-experiments) — Lie Splines
* [InertialScale](https://github.com/jannemus/InertialScale) — IMU to camera time offset and rotation matrix initialization
* [OpenCV](https://opencv.org/) — Well OpenCV ;)
* [Sophus](https://github.com/strasdat/Sophus) — C++ Lie groups
* [GoPro-Telemetry](https://github.com/JuanIrache/gopro-telemetry) — Great JavaScript GoPro telemetry extractor
* [Kontiki](https://github.com/hovren/kontiki) — Spline error weighting, VISFM
* [IMU-TK](https://github.com/Kyle-ak/imu_tk) — Static multi pose IMU calibration
* [Allan variance](https://github.com/gaowenliang/imu_utils) — Gyro noise characterization

---

## Literature and Code

### Libraries

* [1] Theia Multiview Geometry Library: Tutorial & Reference

### Camera Model References

* [2] The **Double Sphere** Camera Model, V. Usenko and N. Demmel and D. Cremers, In 2018 International Conference on 3D Vision (3DV)
* [3] **FoV model**: F. Devernay and O. Faugeras. Straight lines have to be straight. Machine vision and applications, 13(1):14–24, 2001.
* [4] **Extended unified**: B. Khomutenko, G. Garcia, and P. Martinet. An enhanced unified camera model. IEEE Robotics and Automation Letters, 1(1):137–144, Jan 2016.
* [5] **Division undistortion**: "Simultaneous linear estimation of multiple view distortion" by Andrew Fitzgibbon, CVPR 2001.
* [6] **Fisheye**: Kannala, Juho, and Sami S. Brandt. "A generic camera model and calibration method for conventional, wide-angle, and fish-eye lenses." IEEE transactions on pattern analysis and machine intelligence 28.8 (2006): 1335–1340.

### IMU Calibration References

* [11] D. Tedaldi, A. Pretto and E. Menegatti, "A Robust and Easy to Implement Method for IMU Calibration without External Equipments". In: Proceedings of the IEEE International Conference on Robotics and Automation (ICRA 2014), May 31 – June 7, 2014 Hong Kong, China, Page(s): 3042–3049.

### Misc References

* [7] Mustaniemi J., Kannala J., Särkkä S., Matas J., Heikkilä J. "Inertial-Based Scale Estimation for Structure from Motion on Mobile Devices", International Conference on Intelligent Robots and Systems (IROS), 2017
* [8] Efficient Derivative Computation for Cumulative B-Splines on Lie Groups, C. Sommer, V. Usenko, D. Schubert, N. Demmel, D. Cremers, In 2020 Conference on Computer Vision and Pattern Recognition (CVPR)
* [9] Larsson, Viktor, Zuzana Kukelova, and Yinqiang Zheng. "Making minimal solvers for absolute pose estimation compact and robust." Proceedings of the IEEE International Conference on Computer Vision. 2017.
* [10] Hannes Ovrén and Per-Erik Forssén. Spline Error Weighting for Robust Visual-Inertial Fusion. In Proceedings of the IEEE on Computer Vision and Pattern Recognition (CVPR), June 2018.

---

## Working on / ToDo / Contributions Welcome

**v0.1**
* [x] Code cleanup, add license header
* [x] Use different initialization for linear mode
* [x] Use more generic JSON meta data interface, so that others cameras can be calibrated that come with different telemetry formats
* [x] Write example for the calibration of a Smartphone
* [x] Rolling shutter calibration -> first resolve problems with templated spline functions
* [x] Add readout time as a optimizable parameter -> not working well, probably residual weighting needs to be improved
* [x] Allan variance -> imu_utils
* [x] Support AprilTag board from Kalibr to record same datasets
* [x] Calibrate axis misalignment and so on with MultiPoseOptimization from imu_tk
* [x] Include IMU axis and scale in spline error functions
* [x] Beautify logs
* [x] Cleanup

**v0.2**
* [x] Model bias over time with a R3 spline
* [ ] Pose estimation with UPNP or MLPnP to support arbitrary camera types. Right now: undistortion and then using vanilla PnP --> will lead to problems for Ultra Wide Angle fisheye lenses (e.g. GoPro Max or potentially Max lens mod)
* [ ] Pose estimation with RSPnP
* [ ] Use only bearings in spline reproj error -> local tangent reprojection error
* [ ] Accurate checkerboard detector (OpenCV has findCheckerboardSB. I integrated a first version but results were weird. Re-check...)
* [ ] Extend to multi-camera systems
* [x] Docker?
* [ ] Add more camera models -> Scaramuzza omni model, ...
* [x] Integrate updated version of spline optimizer

**misc**
* [ ] Put together a little paper on how this all works

---

## Citation

If this tool helped you and you are using it in your work, consider citing it as follows:

```bibtex
@misc{OpenICC,
  author = {Steffen Urban},
  title = {OpenICC: An Open IMU and Camera Calibrator},
  howpublished = "\url{https://github.com/urbste/OpenImuCameraCalibrator}",
}
```
