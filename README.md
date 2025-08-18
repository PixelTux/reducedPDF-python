# ReducedPDF 🗃️

**A user-friendly GUI tool for compressing PDF files effortlessly.**

ReducedPDF is a Python-based application that simplifies PDF compression using [Ghostscript](https://www.ghostscript.com/). It’s designed for users who prefer a graphical interface over ghostscript command-line tools, making it easy to reduce PDF file sizes without technical hassle. Ideal for anyone seeking a simple, no-fuss solution.

---

## ✨ Features
- **Intuitive GUI**: No command-line knowledge required—just point, click, and compress.
- **Efficient Compression**: Leverages Ghostscript for reliable, high-quality results with multiple compression levels (screen, ebook, printer, prepress).
- **Cross-Platform Compatibility**: Works seamlessly on Linux, macOS, and Windows.
- **Automatic File Naming**: Generates unique output file names to avoid overwriting originals.
- **Size Reduction Feedback**: Displays original and compressed sizes, along with the percentage reduction, after compression.
- **Error Handling**: User-friendly messages for missing files or dependencies.

---

## 🚀 Getting Started

### Prerequisites
ReducedPDF requires the following dependencies, which may need to be installed depending on your system:

- **Python 3.x**: Download and install from [python.org](https://www.python.org/downloads/) if not already present. Ensure Tkinter (Python's GUI library) is included (usually bundled with standard Python installations, but may require additional setup on Linux).
- **Ghostscript**: Required for PDF compression. Download from [ghostscript.com](https://www.ghostscript.com/download/gsdnld.html) for Windows, or install via your package manager on Linux (e.g., `apt`, `dnf`, `pacman`) or macOS (e.g., `brew`). Ensure the `gs` command is in your system PATH.
- **Tkinter (Linux-specific)**: On Linux, you may need to install Tkinter separately using your package manager (e.g., `python3-tk` on Debian/Ubuntu, `python3-tkinter` on Fedora, or `tk` on Arch Linux).

Verify installations:
- Python: `python3 --version` or `python --version`
- Ghostscript: `gs --version`
- Tkinter: `python -c "import tkinter; print('Tkinter is installed')"`

---

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/PixelTux/reducedPDF-python.git
   ```

2. **Navigate to the Project Folder**:
   ```bash
   cd reducedPDF-python
   ```

3. **Run the Application**:
   ```bash
   python reducedPDF.py  # Or python3 on some systems
   ```

---

## 📸 Interface Preview
![ReducedPDF Interface](img/screen/reducedPDF.png)

---

## 📌 Usage
1. Launch the application using the command above.
2. Click "Browse" to select a PDF file.
3. Choose a compression level:
   - **Screen**: Lowest quality, smallest file size (optimized for web viewing).
   - **Ebook**: Balanced quality for e-readers.
   - **Printer**: Good for printing.
   - **Prepress**: Highest quality, larger files.
4. Click "Compress". The compressed file will be saved in the same folder as the original, with a name like `<my_file_name>_ebook_comp.pdf` (appended with the compression level and a number if duplicates exist).
5. A success message will show the original size, compressed size, reduction percentage, and save location.

---

## 🔧 Troubleshooting
- **Ghostscript Not Found**: Ensure `gs --version` works in your terminal/command prompt. If not, reinstall Ghostscript and verify it’s in your system PATH.
- **Tkinter Import Error**: Confirm Tkinter is installed. On Linux, install the relevant package (e.g., `python3-tk` or `python3-tkinter`). On Windows/macOS, reinstall Python from [python.org](https://www.python.org/downloads/) with Tkinter support enabled.
- **Compression Fails**: Check if the PDF is corrupted or password-protected (ReducedPDF doesn't support encrypted files).
- For other issues, open a GitHub issue with details about your OS and error message.

---

## 🤝 Contributing
Contributions are welcome! Feel free to:
- Open an issue for bugs, features, or suggestions.
- Submit a pull request with improvements (e.g., new features, bug fixes, or better cross-platform support).

Please follow standard Python coding conventions and test on your platform.

---

## 📜 License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
