# Simple GUI that uses ghostscript to compress a PDF

# It’s designed for users who prefer a graphical interface
# over ghostscript command-line tools, making it easy to reduce PDF file
# sizes without technical hassle.

# Importing modules
import tkinter as tk
from tkinter import Button, Frame, filedialog, messagebox
import os
import subprocess

class ReducePDFApp:
    def __init__(self, master):
        # Defining custom colors
        self.color_green = "#6CC86D"
        self.color_blue = "#1296CE"
        self.color_white = "#FBFBFF"
        self.color_black = "#040F16"
        self.color_grey = "#DDDEE2"

        # Define dictionaries for file info
        self.original_file = {}
        self.compressed_file = {}

        # Set some custom default values
        self.master = master
        master['bg'] = self.color_white
        master.geometry("1000x620")
        master.option_add("*font", "Times 12")
        master.option_add("*background", self.color_white)
        master.option_add("*fg", self.color_black)

        # Title
        master.title("reducePDF - Reduce the size of your PDF")

        # Creating Frames, which can expand according to the size of the window
        pane_title_label = Frame(master)
        pane_title_label.pack(fill="x", padx=10, pady=35, side="top")

        pane_select_pdf = Frame(master)
        pane_select_pdf.pack(fill="x", padx=10, pady=5, side="top")

        pane_quality_options = Frame(master)
        pane_quality_options.pack(fill="x", padx=6, pady=5, side="top")

        pane_output_label = Frame(master)
        pane_output_label.pack(fill="x", padx=10, pady=20, side="top")

        # App name
        tk.Label(pane_title_label, text="reducePDF", font=("Times New Roman", 26, "italic", "bold"), bg=self.color_white).pack(fill="both", expand=False)
        tk.Label(pane_title_label, text="Reduce the size of your PDF", font=("Times New Roman", 11, "italic"), bg=self.color_white, fg=self.color_green).pack(fill="both", expand=False)

        # Select a PDF file
        self.original_file['path'] = tk.StringVar()
        self.new_file_name = tk.StringVar()
        tk.Label(pane_select_pdf, text="Select a PDF:", width=18, bg=self.color_white).pack(side='left', expand=False)
        tk.Entry(pane_select_pdf, textvariable=self.original_file['path'], state="readonly", readonlybackground=self.color_white).pack(side='left', expand=True, fill="x")
        tk.Button(pane_select_pdf, text="Browse", command=self.browse_pdf, background=self.color_grey, activebackground=self.color_blue).pack(side='right', expand=False, fill="x")

        # Compression quality options
        self.compression_quality = tk.StringVar(value="ebook")

        # Create toggle buttons (radio buttons styled as buttons)
        tk.Radiobutton(pane_quality_options, text="screen", value="screen", variable=self.compression_quality, indicatoron=0, width=7, pady=2, relief="raised", background=self.color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side='left', expand=True, fill="x", padx=2)
        tk.Radiobutton(pane_quality_options, text="ebook", value="ebook", variable=self.compression_quality, indicatoron=0, width=7, pady=2, relief="raised", background=self.color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side='left', expand=True, fill="x", padx=2)
        tk.Radiobutton(pane_quality_options, text="printer", value="printer", variable=self.compression_quality, indicatoron=0, width=7, pady=2, relief="raised", background=self.color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side='left', expand=True, fill="x", padx=2)
        tk.Radiobutton(pane_quality_options, text="prepress", value="prepress", variable=self.compression_quality, indicatoron=0, width=7, pady=2, relief="raised", background=self.color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side='left', expand=True, fill="x", padx=2)

        # Add a label to show the current selection
        tk.Label(pane_output_label, text="Level of compression:", bg=self.color_white).pack()
        self.output_label = tk.Label(pane_output_label, text=self.compression_quality.get().upper(), bg=self.color_green)
        self.output_label.pack()

        # Set the command to update the label when a button is toggled
        self.compression_quality.trace("w", self.update_label)

        # Compress button
        tk.Button(master, text="Compress", command=self.compress_pdf, background=self.color_grey, height=2, width=15, activebackground=self.color_blue, borderwidth=10).pack(side='top', expand=False, pady=20)

    # Update the selected label with the selected value
    def update_label(self, *args):
        self.output_label.configure(text=self.compression_quality.get().upper(), bg=self.color_green)

    # Browse to the PDF
    def browse_pdf(self):
        pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_file:
            self.original_file['path'].set(pdf_file)
            self.original_file['folder'] = os.path.dirname(self.original_file['path'].get())

    # Auto select the file name based on the compression level
    def save_as(self):
        basename = os.path.splitext(os.path.basename(self.original_file['path'].get()))[0] + '_' + self.compression_quality.get() + '_comp'
        self.new_file_name.set(basename)
        loop_number = 1
        file_name = os.path.join(self.original_file['folder'], self.new_file_name.get() + ".pdf")
        while os.path.isfile(file_name):
            self.new_file_name.set(f"{basename}_({loop_number})")
            file_name = os.path.join(self.original_file['folder'], self.new_file_name.get() + ".pdf")
            loop_number += 1
        self.new_file_name.set(self.new_file_name.get() + '.pdf')

    # Auto select the unit to use for the file size (using 1024 for binary prefixes)
    def get_unit(self, bytes_size):
        size = bytes_size
        memory_units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while size >= 1024:
            size /= 1024
            i += 1
        return {"size": format(size, '.2f'), "unit": memory_units[i]}

    # Get compression change in percentage (positive for reduction)
    def get_change(self, old_size, new_size):
        if old_size == 0:
            return 0.0
        change = (old_size - new_size) / old_size * 100.0
        return format(change, '.2f')

    # Compress the PDF
    def compress_pdf(self):
        # Check that a PDF file has been selected
        if not self.original_file['path'].get():
            messagebox.showwarning("Missing PDF File", "Please select a PDF file")
            return

        self.save_as()

        # Compose and run the ghostscript command
        self.compressed_file['path'] = os.path.join(self.original_file['folder'], self.new_file_name.get())
        gs_cmd = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS=/{self.compression_quality.get()}",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={self.compressed_file['path']}",
            self.original_file['path'].get()
        ]

        try:
            subprocess.run(gs_cmd, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Compression Error", f"Failed to compress PDF: {e}")
            return
        except FileNotFoundError:
            messagebox.showerror("Ghostscript Not Found", "Ghostscript is not installed or not in PATH.")
            return

        # Get the sizes
        self.original_file['size'] = os.path.getsize(self.original_file['path'].get())
        self.compressed_file['size'] = os.path.getsize(self.compressed_file['path'])

        # Get change in percentage (reduction)
        change = self.get_change(self.original_file['size'], self.compressed_file['size'])

        # Auto select readable size and unit as dictionary [size, unit]
        self.original_file.update(self.get_unit(self.original_file['size']))
        self.compressed_file.update(self.get_unit(self.compressed_file['size']))

        # Compose the message to print in the message box
        m_original = f"Original size: {self.original_file['size']} {self.original_file['unit']}\n"
        m_compressed = f"Compressed size: {self.compressed_file['size']} {self.compressed_file['unit']}\n"
        m_change = f"Reduced by: {change}%\n"
        m_save_in = f"Saved in: {self.compressed_file['path']}"
        m_all = m_original + m_compressed + m_change + m_save_in

        # Message box after successful compression
        messagebox.showinfo("Success", m_all)

root = tk.Tk()
app = ReducePDFApp(root)
root.mainloop()
