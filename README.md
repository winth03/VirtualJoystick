# VirtualJoystick

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?style=flat-square)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Framework-Kivy-green.svg?style=flat-square)](https://kivy.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg?style=flat-square)](https://docs.microsoft.com/en-us/windows/)

## Project Description

VirtualJoystick is a lightweight, always-on-top overlay application designed for Windows, enabling users to control a virtual Xbox 360 gamepad using on-screen joysticks, buttons, and D-pads. Built with Kivy and `vgamepad`, this utility provides a customizable and persistent virtual input solution, ideal for scenarios requiring a touch-friendly gamepad interface or an overlay for various applications.

The application creates a borderless, shaped, and transparent window that stays on top of other applications, allowing for seamless integration into your workflow. Users can freely reposition the virtual joystick and button widgets, with their layout automatically saved for future sessions.

## Features

*   **Virtual Xbox 360 Gamepad Emulation**: Utilizes `vgamepad` to create and control a virtual Xbox 360 controller, compatible with most PC games and applications that support XInput.
*   **Customizable On-Screen Widgets**: Provides distinct widgets for left joystick, right joystick, action buttons (e.g., A, B, X, Y), and a D-pad.
*   **Overlay Interface**: The Kivy window is configured as borderless, shaped, and always-on-top, providing a transparent overlay that doesn't obstruct underlying applications.
*   **Drag-and-Drop Layout**: Freely drag and reposition all virtual control widgets (joysticks, buttons, D-pads) on the screen to suit your preference.
*   **Persistent Layout**: Widget positions are automatically saved and loaded across sessions using `src/save.py`, ensuring your custom layout is preserved.
*   **Dynamic Window Resizing**: Automatically adapts to the screen resolution and allows for custom padding.
*   **Dynamic Masking**: Uses `src/image.py` to generate a dynamic mask (`temp_mask.png`) for the shaped window, allowing for custom window shapes beyond a simple rectangle.
*   **Window Dragging**: The entire overlay window can be dragged and repositioned on the screen.

## Tech Stack

*   **Python**: Primary programming language.
*   **Kivy**: Open-source Python library for rapid development of applications that make use of novel user interfaces, such as multi-touch apps.
*   **vgamepad**: Python library for creating and controlling virtual Xbox 360 gamepads.
*   **pywin32**: Python for Windows extensions, used for Windows API interactions (`win32gui`, `win32api`, `win32con`) such as setting window properties and getting screen metrics.

## Prerequisites

This application is designed for **Windows operating systems only** due to its reliance on `pywin32` and `vgamepad`.

Before running VirtualJoystick, ensure you have the following installed:

*   **Python 3.x**: Download from [python.org](https://www.python.org/downloads/).
*   **Required Python Packages**:
    *   `kivy`
    *   `vgamepad`
    *   `pywin32`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/winth03/VirtualJoystick.git
    cd VirtualJoystick
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # On Windows
    # source venv/bin/activate # On macOS/Linux
    
    pip install kivy vgamepad pywin32
    ```

## Usage

To start the VirtualJoystick application, simply run the `main.py` script:

```bash
python src/main.py
```

Once launched:

1.  A transparent, always-on-top overlay window will appear.
2.  You will see several virtual control widgets:
    *   A left joystick on the left side.
    *   A right joystick on the right side.
    *   A set of action buttons (A, B, X, Y, etc.) in the center-right.
    *   A D-pad in the center-left.
3.  **Reposition Widgets**: Click and drag any of the joysticks, buttons, or D-pad widgets to move them to your desired position. Their positions will be automatically saved.
4.  **Reposition Window**: Click and drag any empty part of the window (or the `exclude` areas not covered by widgets) to move the entire overlay window.
5.  **Interact**: Use your mouse (or touch if on a touch-enabled device) to interact with the virtual controls. Moving the joysticks, pressing buttons, or activating D-pad directions will send corresponding inputs to the virtual Xbox 360 gamepad.
6.  **"Edit" Button**: The "Edit" button in the top-left corner is part of the excluded elements for dragging. Its functionality is not fully described but typically toggles an edit mode.
7.  **"Close" Button**: The "Close" button in the top-right corner will terminate the application.

## Project Structure

The repository is organized as follows:

```
.
├── .gitignore               # Specifies intentionally untracked files to ignore
└── src/                     # Main source code directory
    ├── buttons.py           # Kivy widget for managing virtual buttons and D-pads
    ├── image.py             # Utility for dynamic image processing and mask generation
    ├── img/                 # Contains various image assets for joystick handles and backgrounds
    │   ├── Joystick.png
    │   ├── JoystickSplitted.png
    │   ├── LargeHandleFilled.png
    │   ├── LargeHandleFilledGrey.png
    │   ├── SmallHandle.png
    │   ├── SmallHandleFilled.png
    │   └── SmallHandleFilledGrey.png
    ├── joystick.py          # Kivy widget for managing a single virtual joystick
    ├── main.py              # The main application entry point and Kivy app setup
    └── save.py              # Handles saving and loading application configuration (e.g., widget positions)
```

## License

This project is currently not licensed. Please contact the repository owner for licensing information.