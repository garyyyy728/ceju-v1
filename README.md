# Web-based YOLOv5 Object Detection Application

This is a web-based application for object detection using YOLOv5. The application allows users to perform real-time object detection using their webcam directly from a web browser.

## Features

- Real-time object detection using YOLOv5
- User-friendly web interface
- Display of detection results with bounding boxes and labels
- Start and stop video stream with a single click

## Requirements

- Python 3.6 or higher
- Flask
- PyTorch
- OpenCV
- PIL (Pillow)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/garyyyy728/ceju-v1.git
   cd ceju-v1
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the YOLOv5 model weights and place them in the `pt` directory.

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

## Using the Web Interface

1. Click the "Start" button to start the webcam video stream.
2. The application will perform real-time object detection and display the results on the video.
3. Click the "Stop" button to stop the video stream.

## Troubleshooting

- **Webcam not accessible**: Ensure that your browser has permission to access the webcam.
- **Server not starting**: Check if the required dependencies are installed correctly.
- **Detection results not accurate**: Ensure that the YOLOv5 model weights are correctly placed in the `pt` directory.

## Common Issues

- **Permission Denied**: If you encounter a permission denied error, try running the command with `sudo`.
- **Module Not Found**: Ensure that all required modules are installed by running `pip install -r requirements.txt`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
