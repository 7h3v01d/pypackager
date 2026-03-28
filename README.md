# 🚀 PyPackager – Python to EXE Builder

**A friendly, all-in-one GUI for turning Python scripts into standalone Windows .exe files.**

No command line needed! Perfect for beginners, students, and developers who want a simple and beautiful way to package their Python apps.

<img width="1920" height="1040" alt="screenshot" src="https://github.com/user-attachments/assets/7517162b-4529-491c-b7d5-6435d53d3041" />

## ✨ Features

- **Beautiful modern GUI** with dark theme and smooth animations
- **Drag & Drop** support for scripts and icons
- **One-File** or Folder mode
- **Windowed** (no console) or **Console** mode
- **Custom Icon** support (with built-in PNG → ICO converter)
- **Extra files/folders** support (images, data, multiple .py files)
- **Hidden imports** and advanced PyInstaller options
- **App metadata** (Product Name, Company, Version, Description)
- **Preset save/load** (save your build settings)
- **Real-time build log** with progress bar
- **Built-in PNG to ICO converter** using Pillow

## 📋 Requirements

- **Python 3.8+**
- Windows (recommended for best .exe compatibility)

### Install Dependencies

```bash
pip install -r requirements.txt
```
## 🚀 How to Use

1. Install the requirements:
```Bash
pip install -r requirements.txt
```
2. Run PyPackager:
```Bash
python pyinstaller_gui.py
```
3. Build your EXE:

- Select your main .py file
- Choose an output name
- (Optional) Add icon, extra files, or advanced options
- Click BUILD EXE!

Your executable will appear in the dist folder (or the folder you specified).

## 🎨 PNG → ICO Converter
PyPackager includes a handy built-in tool to convert any PNG image into a proper Windows .ico file with multiple sizes.

## 🛠️ Advanced Options

- One-File Mode (single .exe)
- Windowed / Console mode
- UPX compression (if UPX is installed)
- Hidden imports
- Extra data files
- Version information (shows in file properties)

## 📁 Project Structure

```text
PyPackager/
├── pyinstaller_gui.py     # Main GUI application
├── requirements.txt
├── README.md
└── (your Python scripts here)
```
## ⚠️ Important Notes

- The first build may take a while (PyInstaller downloads and bundles Python).
- One-file mode creates larger but easier-to-share executables.
- Some antivirus software may flag PyInstaller EXEs as false positives — this is common and usually safe.

## 🐛 Troubleshooting

- EXE crashes immediately: Switch to Console mode to see the error.
- ModuleNotFoundError: Add the missing module in "Hidden Imports".
- Missing files: Use "Multi-file project" mode and add your resources.
- EXE too big: Enable UPX compression (requires UPX installed separately).

## Contribution Policy

Feedback, bug reports, and suggestions are welcome.

You may submit:

- Issues
- Design feedback
- Pull requests for review

However:

- Contributions do not grant any license or ownership rights
- The author retains full discretion over acceptance and future use
- Contributors receive no rights to reuse, redistribute, or derive from this code

---

License
This project is not open-source.

It is licensed under a private evaluation-only license.
See LICENSE.txt for full terms.
