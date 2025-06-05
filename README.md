# Python GUI written in PyQt6 for YT-DLP

<!-- TODO: update README -->

## Commands
* Ctrl-V: When entering CTRL-V on GUI automatically sends to Queue
* Auto: When Adding to Queue it will automatically start downloading.
* Clipboard Monitor: Auto adds youtube links, if auto start then will auto download
* Format 1080p: 1080p Download Best
* MKV Remux: Added Toggle
* Embed Subs: Added Toggle
<br>

## Other
* Remember Filename Arguments
* If no Ctrl-V Mode, hitting enter on link text area will add to Status Queue
* Fixed Category Spacing in Status Queue
  
<br>

![Screenshot](.github/image.png)

## Credit
- project basek on work of [Rootkit-](https://github.com/Rootkit-/yt-dlp-gui)
- Ninjad most from fork [dsymbol](https://github.com/dsymbol/yt-dlp-gui)
<br>
<br>
<br>
<br>


_______
# original readme yt-dlp-gui
Graphical interface for the command line tool [yt-dlp](https://github.com/yt-dlp/yt-dlp), which allows users to download 
videos from various [websites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md), including YouTube. 
It is designed to be more user-friendly and accessible for those who are not comfortable using the command line.

## Screenshot
![image](https://github.com/user-attachments/assets/f9cd3e90-dcaa-4ef8-a5e6-94a76a8d8c29)

## Getting Started

There are three ways to get started, depending on your preference and system:

* [`Portable`](#portable) ~ *Windows*
* [`Build`](#build) ~ *Windows & Linux*
* [`Manual`](#manual) ~ *Platform independent*

### Portable

Download the latest portable version from the [releases](https://github.com/matszwe02/yt-dlp-gui/releases/latest) section. 
This will download a ZIP file containing the program files and all necessary dependencies.

*All releases are built and released using GitHub Workflow*

### Build

You **must** have [Python](https://www.python.org/downloads/) 3.9+ installed.

To build yt-dlp-gui from its source code:

1. Clone the repository onto your local machine:

```bash
git clone https://github.com/matszwe02/yt-dlp-gui
cd yt-dlp-gui
```

2. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

3. Use PyInstaller to compile the program:

```bash
cd app
```

#### Linux

```bash
pyinstaller --name=yt-dlp-gui --clean -y app.py
```

#### Windows

```pwsh
pyinstaller --name=yt-dlp-gui --clean -y app.py --icon ./ui/assets/yt-dlp-gui.ico --noconsole
```

4. The executable will be ready at:

```bash
./dist/yt-dlp-gui
```

### Manual

You **must** have [Python](https://www.python.org/downloads/) 3.9+ installed.

1. Clone the repository onto your local machine:

```bash
git clone https://github.com/dsymbol/yt-dlp-gui
cd yt-dlp-gui
```

2. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

3. Run the program:

```bash
cd app
python app.py
```
