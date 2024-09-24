# Pictriever
A python script based off AuroraWright's owocr, which uses Google Lens to extract text from image.

## Features
- Select an area on the screen using a hotkey
- Preprocess the captured image (convert to grayscale and resize)
- Extract text from the image using Google Lens
- Copy the extracted text to the clipboard
- Configurable hotkeys for different actions

## Prerequisites
- Python 3.7 or higher
- Required Python libraries (see Installation section)

## Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/Arikips/Pictriever.git
    cd Pictriever
    ```

2. **Install Required Libraries**

    ```sh
    pip install Pillow pyautogui pyperclip keyboard pyjson5 requests
    ```

## Usage

1. **Configure Hotkeys**

    The default hotkeys are:
    - `ctrl+alt+s` for selecting the area
    - `ctrl+alt+x` for scanning the selected area
    - `ctrl+alt+a` for toggling the autoscan
    - `ctrl+alt+q` for terminating the application

    You can change these hotkeys by editing the `settings.json` file which will be generated in the project directory after the first run.

2. **Run the Script**

    ```sh
    python pictriever.py
    ```

3. **How to Use the Script**

    - **Select Area Hotkey:** Press the hotkey (default `ctrl+alt+s`) to start selecting an area on the screen. Click and drag to draw a rectangle. Release the mouse button to finish the selection. Only the current selection box will be visible.
    - **Scan Area Hotkey:** Press the hotkey (default `ctrl+alt+x`) to capture the selected area, preprocess the image (convert to grayscale and resize to a maximum of 500x500 pixels), extract text using Google Lens, and copy the extracted text to the clipboard. The extracted text will also be printed to the console.
    - **Terminate Script Hotkey:** Press the hotkey (default `ctrl+alt+q`) to terminate the script.


## Credits

Big thanks to [AuroraWright](https://github.com/AuroraWright/owocr) for their amazing work on `owocr` and to Google for their powerful OCR tools.
