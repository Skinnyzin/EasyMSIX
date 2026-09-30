# EasyMSIX

**EasyMSIX** is a lightweight Windows utility designed to simplify the installation of `.msix`, `.msixbundle`, `.appx`, and `.appxbundle` packages. Built with Python and CustomTkinter, it provides an intuitive graphical interface with real-time progress tracking, automatic package details extraction, and seamless file association.

---

## Features

- **One-Click Installation**: Double-click any `.msix` or `.appx` file to install it instantly.
- **Context Menu Integration**: Adds an *"Install with EasyMSIX"* option to the right-click context menu in Windows Explorer.
- **Package Metadata Extraction**: Automatically extracts the app name and embedded icon directly from the package manifest without extracting temporary files to disk.
- **Real-Time Progress**: Displays accurate progress percentages while installing packages via PowerShell.
- **Modern UI**: Built with `CustomTkinter` following Windows dark/light system theme preferences.
- **UAC Elevation**: Prompts for administrator permissions only when required.

---

## Getting Started

### Prerequisites

- **Windows 10/11**
- **Python 3.8+** (if running from source)

### Dependencies

If running from source, install the required packages:

```bash
pip install customtkinter pillow
