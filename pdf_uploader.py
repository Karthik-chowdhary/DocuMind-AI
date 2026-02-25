import os
import shutil
import tkinter as tk
from tkinter import filedialog

def upload_pdf():
    root = tk.Tk()
    root.withdraw()
    
    root.attributes('-topmost',True)
    source_path = filedialog.askopenfilename(
        title = "select pdf to upload",
        filetypes = [("PDF documents","*.pdf")]
    )
    if not source_path:
        print("file uploadation cancelled, no file uploaded.")
        return
    current_dir = os.getcwd()
    
    file_name = os.path.basename(source_path)
    
    pdfs_folder = os.path.join(current_dir,"pdf's")
    if not os.path.exists(pdfs_folder):
        os.makedirs(pdfs_folder)
    
    destination_path = os.path.join(pdfs_folder,file_name)

    try:
        shutil.copy2(source_path,destination_path)
        print("file copied successfully!\n")
    except shutil.SameFileError:
        print(f"the file {file_name} is already in this folder\n.")
    except Exception as e:
        print(f"as error occured: {e}")
    
    pdf_path = destination_path

    return pdf_path

if __name__ == "__main__":
    upload_pdf()