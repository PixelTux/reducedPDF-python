#   Simple GUI that use goscreept to compress a pdf

#   This app is thout for new people in linux that want 
#   to compress a pdf and don't know how to use gosctip

# Importing modules
import tkinter as tk
from tkinter import Button, Frame, filedialog, messagebox
import os
import subprocess

class ReducePDFApp:
    def __init__(self, master):
        # defining custom colors
        self.color_green="#6CC86D"
        color_blue="#1296CE"
        color_white="#FBFBFF"
        color_black="#040F16"
        color_grey="#DDDEE2"
        
        # define the dictionary
        self.original_file = {}
        self.compresed_file = {}

        # set some costum defolt value
        self.master = master
        master['bg']=color_white
        master.geometry("1000x620")
        master.option_add( "*font", "Times 12" )
        master.option_add( "*background", color_white )
        master.option_add( "*fg", color_black )

        # title
        master.title("reducePDF - Reduce the size of your PDF")

        # creating a Frames, which can expand according to the size of the window
        pane_title_label = Frame(master)
        pane_title_label.pack(fill="x", padx=10, pady=35, side="top")

        pane_select_pdf = Frame(master)
        pane_select_pdf.pack(fill="x", padx=10, pady=5, side="top")

        pane_save_pdf = Frame(master)
        pane_save_pdf.pack(fill="x", padx=10, pady=5, side="top")

        pane_quality_options = Frame(master)
        pane_quality_options.pack(fill="x", padx=6, pady=5, side="top")

        pane_output_label = Frame(master)
        pane_output_label.pack(fill="x", padx=10, pady=20, side="top")

        # app name
        tk.Label(pane_title_label, text="reducePDF", font=("Times New Roman", 26,"italic", "bold"), bg=color_white).pack(fill="both", expand=False)
        tk.Label(pane_title_label, text="Reduce the size of your PDF", font=("Times New Roman", 11,"italic"), bg=color_white,fg=self.color_green).pack(fill="both", expand=False)
        
        # select a PDF file
        self.original_file['path'] = tk.StringVar()
        self.compresed_file['name'] = tk.StringVar()
        self.new_file_name = tk.StringVar()
        tk.Label(pane_select_pdf, text="Select a PDF:", width=18, bg=color_white).pack(side='left', expand=False)
        tk.Entry(pane_select_pdf, textvariable=self.original_file['path'], state="readonly", readonlybackground=color_white).pack(side='left', expand=True, fill="x")
        tk.Button(pane_select_pdf, text="Browse", command=self.browse_pdf, background=color_grey, activebackground=color_blue).pack(side='right', expand=False, fill="x")

        # compression quality options
        self.compression_quality = tk.StringVar(value="ebook")

        # create toggle buttons
        self.button_screen = tk.Radiobutton(pane_quality_options, text="screen", value="screen", variable=self.compression_quality, indicatoron=0, width=7,pady=2, relief="raised", background=color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side ='left', expand = True, fill="x", padx=2)
        self.button_ebook = tk.Radiobutton(pane_quality_options, text="ebook", value="ebook", variable=self.compression_quality, indicatoron=0, width=7,pady=2, relief="sunken", background=color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side ='left', expand = True, fill="x", padx=2)
        self.button_printer = tk.Radiobutton(pane_quality_options, text="printer", value="printer", variable=self.compression_quality, indicatoron=0, width=7,pady=2, relief="raised", background=color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side ='left', expand = True, fill="x", padx=2)
        self.button_prepress = tk.Radiobutton(pane_quality_options, text="prepress", value="prepress", variable=self.compression_quality, indicatoron=0, width=7,pady=2, relief="raised", background=color_grey, selectcolor=self.color_green, activebackground=self.color_green).pack(side ='left', expand = True, fill="x",  padx=2)
        
        # add a label to show the current selection
        tk.Label(pane_output_label, text="Level of compression:", bg=color_white).pack()
        self.output_label = tk.Label(pane_output_label, text=self.compression_quality.get().upper(), bg=self.color_green)
        self.output_label.pack()

        # set the command to update the label when a button is toggled
        self.compression_quality.trace("w", self.update_label)

        # compress button
        tk.Button(master, text="Compress", command=self.compress_pdf, background=color_grey, height=2, width=15, activebackground=color_blue, borderwidth=10 ).pack(side='top', expand=False, pady=20)

    # Update the selected lable with the selecte value
    def update_label(self, *args):
        self.output_label.configure(text=self.compression_quality.get().upper(), bg=self.color_green)

    # Browse to the pdf 
    def browse_pdf(self):
        pdf_file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if pdf_file:
            self.original_file['path'].set(pdf_file)
            self.original_file['folder'] = os.path.dirname(self.original_file['path'].get())

    # Auto select the file name based on the compression level
    def save_as(self):
        self.new_file_name.set( os.path.splitext(os.path.basename(self.original_file['path'].get()))[0] + '_' + self.compression_quality.get() + '_comp')
        basename = self.new_file_name.get()    
        while_loop_nuber = 1
        file_name = self.original_file['folder'] + "/" + self.new_file_name.get()+".pdf"
        while os.path.isfile(file_name):
            self.new_file_name.set("{}_({})".format(basename, while_loop_nuber))
            file_name = self.original_file['folder'] + "/" + self.new_file_name.get() + ".pdf"
            while_loop_nuber += 1
        self.new_file_name.set(self.new_file_name.get() + '.pdf')

    # Auto select the unit tu use fore the fiel size 
    def get_unit(self, bytes):
        size = bytes
        memory_units = ['B','KB','MB','GB','TB']
        i = 0
        while size >= 1000:
            size = size/1000
            i += 1 
        return {"size":format(size,'.2f'), "unit":memory_units[i]}
    
    # Get compression change in prcentage 
    def get_change(self, current, previous):
        if current == previous:
            return 100.0
        try:
            return (current - previous) / previous * 100.0
        except ZeroDivisionError:
            return 0

    # Compress the PDF
    def compress_pdf(self):
        # check that a PDF file has been selected
        if not self.original_file['path'].get():
            messagebox.showwarning("Missing PDF Files!!!", "Please select a PDF file")
            return
        
        self.save_as()

        # compouse and run the gosctip
        self.compresed_file['path']= self.original_file['folder'] + "/" + self.new_file_name.get()
        gs_cmd = f"gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/{self.compression_quality.get()} -dNOPAUSE -dQUIET -dBATCH -sOutputFile='{self.compresed_file['path']}' '{self.original_file['path'].get()}'"
        subprocess.run(gs_cmd, shell=True)
        self.save_as()

        # get the size 
        self.original_file['size'] = os.path.getsize(self.original_file['path'].get())
        self.compresed_file['size'] = os.path.getsize(self.compresed_file['path'])

        # get change in percentage [new_size, old_size]
        change = self.get_change(self.compresed_file['size'], self.original_file['size'])
        change = format(change, '.2f')

        # auto select readable size and unit as dictionary [size, unit]
        for x, y in self.get_unit(self.original_file['size']).items():
            self.original_file[x] = y
        for x, y in self.get_unit(self.compresed_file['size']).items():
            self.compresed_file[x] = y

        # compuse the message to print in the message box 
        m_original = "Original size \n" + self.original_file['size'] + self.original_file['unit']+"\n"
        m_compresed = "Compressed size \n"+ self.compresed_file['size'] + self.compresed_file['unit']+"\n"
        m_change = "Change \n" + change + "%" + "\n"
        m_save_in = "Save in \n" + self.compresed_file['path']
        m_all = m_original + m_compresed + m_change + m_save_in

        # Message box after succes compression 
        messagebox.showinfo("Success", f"{m_all}")

root = tk.Tk()
app = ReducePDFApp(root)
root.mainloop()