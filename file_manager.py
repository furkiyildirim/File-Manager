import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import datetime

farfrom = 0
nav_loc = os.getcwd()

# TODO: HATALAR DÜZELECEK VE ARAÇ ÇUBUĞU ÖZELLİKLERİ EKLENECEK VE UYGULAMALARI TREEDEN ÇLAIŞTIRABİLCEĞİZ.

def main():

    root = tk.Tk()
    root.title("Dosya Gezgini")
    root.geometry("700x400")

    # Menü çubuğu
    def new_file():
        global refresh
        global nav_loc
        print('new file initialdir', nav_loc)
        file = filedialog.asksaveasfilename(
            title="Yeni Dosya",
            defaultextension=".txt",
            filetypes=(("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")),
            initialdir = nav_loc
        )
        if file:
            with open(file, "w", encoding="utf-8") as f:
                f.write("")  # boş dosya oluştur
            print("Yeni dosya oluşturuldu:", file)
            refresh()
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Yeni", command=new_file)
    #file_menu.add_command(label="Aç")
    menubar.add_cascade(label="DOSYA", menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Kes")
    edit_menu.add_command(label="Kopyala")
    menubar.add_cascade(label="DUZENLE", menu=edit_menu)

    view_menu = tk.Menu(menubar, tearoff=0)
    view_menu.add_command(label="Liste Görünümü")
    menubar.add_cascade(label="GORUNUM", menu=view_menu)

    root.config(menu=menubar)
    # Top navbar
    def refresh():
        global nav_loc
        if tree.get_children() is not None:
            for item in tree.get_children():
                tree.delete(item)
        for item in os.listdir(nav_loc):
            file_path = nav_loc + '\\' + item
            if os.path.isfile(file_path):
                stat_info = os.stat(file_path)
                file_name = item
                file_type = file_name.split('.')[len(file_name.split('.'))-1]
                if file_type != None and len(file_name.split('.')) == 2:
                    file_types = {
                        # Metin ve doküman
                        ".txt": "Metin Dosyası",
                        ".pdf": "PDF Belgesi",
                        ".doc": "Word Belgesi",
                        ".docx": "Word Belgesi",
                        ".xls": "Excel Tablosu",
                        ".xlsx": "Excel Tablosu",
                        ".ppt": "PowerPoint Sunumu",
                        ".pptx": "PowerPoint Sunumu",

                        # Kod ve betik
                        ".py": "Python Dosyası",
                        ".js": "JavaScript Dosyası",
                        ".html": "HTML Dosyası",
                        ".css": "CSS Dosyası",
                        ".c": "C Kaynak Dosyası",
                        ".cpp": "C++ Kaynak Dosyası",
                        ".java": "Java Dosyası",
                        ".php": "PHP Dosyası",

                        # Sıkıştırılmış arşiv
                        ".zip": "ZIP Arşivi",
                        ".rar": "RAR Arşivi",
                        ".7z": "7-Zip Arşivi",
                        ".tar": "TAR Arşivi",
                        ".gz": "GZip Arşivi",

                        # Resim
                        ".jpg": "JPEG Resmi",
                        ".jpeg": "JPEG Resmi",
                        ".png": "PNG Resmi",
                        ".gif": "GIF Resmi",
                        ".bmp": "Bitmap Resmi",
                        ".svg": "Vektör Resmi",

                        # Ses
                        ".mp3": "MP3 Ses",
                        ".wav": "WAV Ses",
                        ".ogg": "OGG Ses",
                        ".flac": "FLAC Ses",

                        # Video
                        ".mp4": "MP4 Video",
                        ".avi": "AVI Video",
                        ".mkv": "MKV Video",
                        ".mov": "QuickTime Video",
                        ".wmv": "Windows Media Video",

                        # Çalıştırılabilir / Sistem
                        ".exe": "Windows Uygulaması",
                        ".msi": "Windows Kurulum Dosyası",
                        ".bat": "Batch Betiği",
                        ".sh": "Shell Script",
                        ".apk": "Android Uygulaması",
                        ".iso": "Disk İmajı",
                    }

                    file_size = stat_info.st_size
                    mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    tree.insert("", tk.END, values=(file_name, mod_time, file_types.get(f'.{file_type}'), f"{file_size} BYTE"))
                    tree.pack(fill=tk.BOTH, expand=True)
                else:
                    file_size = stat_info.st_size
                    mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    tree.insert("", tk.END, values=(file_name, mod_time, 'Dosya', f"{file_size} BYTE"))
                    tree.pack(fill=tk.BOTH, expand=True)

            if os.path.isdir(file_path):
                stat_info = os.stat(file_path)
                file_name = item
                file_size = stat_info.st_size
                mod_time = datetime.datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                tree.insert("", tk.END, values=(file_name, mod_time, "Dosya Klasörü", f"{file_size} BYTE"))
                tree.pack(fill=tk.BOTH, expand=True)

    def back(btn):
        global farfrom
        global nav_loc
        # nav location
        #current_location = os.getcwd()
        farfrom += 1
        back_location = nav_loc.split('\\')[0:len(os.getcwd().split('\\'))-farfrom]
        print("navloc: ", nav_loc)
        if len(back_location) == 0:
                back_btn.config(state="disabled")
                farfrom = 0
        else:
            print(farfrom)
            l = ""
            for loc in back_location:
                l += loc+'\\'
            print(l)

            nav_loc = l
            path_entry.config(state="normal")
            path_entry.delete(0, tk.END)
            path_entry.insert(0, l)
            path_entry.config(state="disabled")

        refresh()
    def on_click(event):
            global nav_loc
            global farfrom
            item_id = tree.identify_row(event.y)
            if item_id:
                values = tree.item(item_id, "values")
                # open directory
                if values[2] == "Dosya Klasörü" and os.path.isdir(nav_loc + '\\'+ values[0]):
                    farfrom -= 1
                    nav_loc = nav_loc[0: len(nav_loc)-1] + '\\' + values[0] + '\\'
                    path_entry.config(state="normal")
                    path_entry.delete(0, tk.END)
                    path_entry.insert(0, nav_loc)
                    path_entry.config(state="disabled")
                    print("on click",nav_loc)
                else:
                    os.startfile(f'{nav_loc+values[0]}')
                # open file

            refresh()
    toolbar = tk.Frame(root, bd=1, relief=tk.SUNKEN)
    path_entry = tk.Entry(toolbar)
    path_entry.insert(0, f"{os.getcwd()}")
    path_entry.config(state="disabled")


    back_btn = tk.Button(toolbar, text="<",command=lambda: back(back_btn))
    refresh_b = tk.Button(toolbar, text="⟳", command=refresh)

        # file list

    back_btn.pack(side=tk.LEFT, padx=2, pady=2)
    refresh_b.pack(side=tk.LEFT, padx=2, pady=2)
    path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)

    toolbar.pack(side=tk.TOP, fill=tk.X)

    # Right panel (Treeview table)
    right_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    columns = ("Ad", "Değiştirme Tarihi", "Tür", "Boyut")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.W, width=150)

    tree.bind("<Button-1>", on_click)


    # Current location files

    refresh()


    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        ...
