<h1 align="center">
  <img src="assets/BCSS Logo.png"
       alt="BCSS Logo"
       width="500">
</h1>

# Body-Controlled Subway Surfers

Control Subway Surfers (or other keyboard-based games) using your body movements with a webcam.

This project uses MediaPipe Pose to detect your body position in real time and converts your movements into keyboard and mouse inputs.

![Subway Surfers](assets/subwaysurfers.gif)

## Features
- Move left and right by shifting your body.
- Jump by raising your body.
- Crouch by lowering your body.
- The gesture of raising the left hand triggers a mouse click.
- The gesture of raising the left hand presses the space bar(use hoverboard).
- Runs entirely with a standard webcam.

## How It Works

The program detects your pose using MediaPipe and tracks:

- Shoulder positions to estimate the center of your body.
- Hand positions for gesture detection.
- The camera image is divided into regions.

## Installation and Usage

- Clone the repository:
```
git clone https://github.com/yourusername/body-controlled-subway-surfers.git
cd body-controlled-subway-surfers
```
- Install the dependencies:
```
pip install -r requirements.txt
```
- Run python file:
```
python main.py
```
- Press Q to quit.

## Requirements
- Python 3.10+
- Webcam
- Windows (tested)

### Libraries:
- OpenCV
- MediaPipe
- PyAutoGUI

## License
This project is available under the MIT License.
