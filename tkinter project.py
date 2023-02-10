# SOURCE

# https://www.tutorialspoint.com/creating-a-browse-button-with-tkinter#




from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import shutil
import os



SOURCE_PATH = ''
DESTINATION_BASE_PATH = r'D:/destination_folder/'
DESTINATION_SIZE_LIMIT = 2 * 1024

window = Tk()
window.geometry("700x350")
window.title('Cloud Computing Project')

def open_file():
    file = filedialog.askopenfile(mode='r', filetypes=[('All Files', '*.*')])
    if file:
        file.close()
        SOURCE_PATH = file.name
        SOURCE_FILE_SIZE = os.path.getsize(SOURCE_PATH)
        print("File Size is ===>> %.2f KBs" % (SOURCE_FILE_SIZE/1024))

        if size_validation(SOURCE_FILE_SIZE):
            global DESTINATION_BASE_PATH
            DESTINATION_PATH = DESTINATION_BASE_PATH + str(file.name).split('/')[-1]
            shutil.copyfile(SOURCE_PATH, DESTINATION_PATH)
            print('DONE!')
        else:
            print('FILE SIZE TOO LARGE. TRANSFER TERMINATED!')



def size_validation(SOURCE_FILE_SIZE):
    folder_size = 0
    # Folderpath = 'C:/Users/Geetansh Sahni/Documents/R'

    for path, dirs, files in os.walk(DESTINATION_BASE_PATH):
        for f in files:
            fp = os.path.join(path, f)
            folder_size += os.path.getsize(fp)

    current_folder_size = folder_size/(1024*1024)
    size_after_transfer = current_folder_size + (SOURCE_FILE_SIZE/1024)
    
    if size_after_transfer > DESTINATION_SIZE_LIMIT:
        return False
    else:
        print(f"Folder size: %.2f MBs" % size_after_transfer)
        return True



label = Label(window, text="Click the Button to browse the Files", font=('Georgia 13'))
label.pack(pady=10)

Dest_Folder_Size = os.path.getsize(DESTINATION_BASE_PATH)
label2 = Label(window, text=f"Current Folder Size = {Dest_Folder_Size/(1000)} KBs", font=('Georgia 13'))
label2.pack(pady=10)

# Create a Button
ttk.Button(window, text="Browse", command=open_file).pack(pady=20)

window.mainloop()