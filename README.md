# MyVideoPlayer

MyVideoPlayer is a modern, feature-rich desktop video player application built using **Python** and **PyQt6**. It offers a smooth playback experience with intuitive controls, thumbnail previews, and comprehensive keyboard support.

## 🚀 Features

-   **Playback Controls**: Play, Pause, and Stop video playback.
-   **Smart Seek Bar**:
    -   Click and drag to seek.
    -   **Hover Preview**: View a thumbnail preview of the video at the cursor position before seeking.
-   **Fullscreen Mode**: Immersive viewing experience with a toggleable fullscreen mode.
-   **Volume Control**: Adjust audio volume using the dial or keyboard shortcuts.
-   **Playlist & Network Support**: Manage playlists and stream from network devices (UPnP).
-   **Keyboard Shortcuts**: Control the player entirely with your keyboard.

## 🛠️ Installation

### Prerequisites
-   Python 3.x
-   `pip` package manager

### Steps

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/smitkpatel16/VideoPlayer.git
    cd VideoPlayer
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🎮 Usage

1.  **Run the application**:
    ```bash
    python Main.py
    ```

2.  **Open Media**:
    -   Use `File > Open` to select a video file.
    -   Or select a file from the Playlist/Network tree if available.

3.  **Controls**:
    -   Use the on-screen buttons to control playback.
    -   Hover over the progress bar to see a timestamped thumbnail.

### ⌨️ Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| **Space** | Play / Pause |
| **F** | Toggle Fullscreen |
| **Esc** | Exit Fullscreen |
| **Left Arrow** | Seek Backward (5s) |
| **Right Arrow** | Seek Forward (5s) |
| **Up Arrow** | Increase Volume |
| **Down Arrow** | Decrease Volume |

## 🧪 Testing

The project includes a `testBench` with unit tests for key features.

To run the tests:
```bash
python -m unittest discover testBench
```

## 📦 Dependencies

-   `PyQt6`
-   `opencv-python` (for thumbnail extraction)
-   `ffmpeg-python`
-   `upnpy`
-   `lxml`

See `requirements.txt` for the full list.

## 🤝 Contributing

Contributions are welcome! Please feel free to obtain a copy of the project and submit pull requests.

## 📄 License

This project is licensed under the MIT License.

## 📸 Preview

![Video Player Preview](https://github.com/smitkpatel16/VideoPlayer/blob/main/Preview.png)