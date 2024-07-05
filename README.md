# Real-Time Frame Processing with Flask

## Overview

This project demonstrates real-time frame processing using Flask. It integrates computer vision techniques to process frames from a video stream in real-time. This can be useful for various applications such as object detection, motion tracking, and more.

## Features

- **Real-Time Processing**: Processes video frames in real-time.
- **Flask Integration**: Uses Flask to create a web interface for video stream display.
- **Easy Setup**: Simple to install and run with minimal dependencies.
- **Extensible**: Easily extend the processing logic to include custom algorithms.

## Demo

<video width="600" controls autoplay>
  <source src="videos/working.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

Watch the [demo video](videos/working.mp4) to see the project in action.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/omartarekmoh/Real-Time-Frame-Processing-with-Flask.git
    cd Real-Time-Frame-Processing-with-Flask
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```bash
    python app.py
    ```

## Usage

1. After running the application, open your web browser and go to `http://127.0.0.1:5000/`.
2. You should see the video stream being processed in real-time.

## Project Structure

- `app.py`: The main Flask application file.
- `static/`: Contains static files like CSS and JavaScript.
- `templates/`: Contains HTML templates for the web interface.
- `videos/`: Contains demo videos and other video-related resources.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Special thanks to all contributors and the open-source community.
- This project was inspired by various real-time processing applications and frameworks.
