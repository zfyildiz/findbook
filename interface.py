import tkinter as tk
from tkinter import *
from tkinter import Button, messagebox
from project import search
from PIL import ImageTk, Image

# pencere oluşturma
window = tk.Tk()
# Başlık ekleme
window.title("FIND BOOK")
# Boyutlandırma
window.geometry("800x650+450+140")
# boyutlandırmayı engelleme
window.resizable(FALSE,FALSE)

# pencerede label oluşturma
text = Label(text="FINDBOOK",
             fg="bisque2",
             bg="aquamarine4",
             width=10,
             height=3,
             padx=400,
             justify="left",
             font=("Times New Roman", "30", "bold underline "))
text.pack()

x = Label(text="KİTAP ARA",
          fg="DodgerBlue4",
          bg="light sky blue",
          padx=400,
          font=("Times New Roman", "20", "bold"))
x.pack()

#Resim ekleme
path = "library.jpg"
img = ImageTk.PhotoImage(Image.open(path))
panel = Label(window, image=img)
panel.pack(side='bottom', fill="both", expand="yes")

#sonuçları message box'ta gösteren fonksiyon
def get_data():
    name = e.get()
    data = f.get()
    result = search(name, data)
    messagebox.showinfo("KİTAP BİLGİLERİ", "BKM KİTAP \n"+result[0]['kitapAdi']+
                        "\n"+result[0]['yayinevi']+"\n"+result[0]['yazar']+"\n"+result[0]['fiyat']+
                        "\n============================\nKİTAP YURDU\n"+result[1]['kitapAdi']+"\n"+
                        result[1]['yayinevi']+"\n"+result[1]['yazar']+"\n"+result[1]['fiyat']+
                        "\n============================\nD&R KİTAP\n"+result[2]['kitapAdi']+"\n"+
                        result[2]['yayinevi']+ "\n"+result[2]['yazar']+"\n"+result[2]['fiyat'])

#Kullanıcıdan kitap adını alan entry
e = Entry(window, width=50)
e.pack()
e.insert(0, "Kitap Adı: ")

#Yayınevi bilgisini alan entry
f = Entry(window, width=50)
f.pack()
f.insert(0, "Yayınevi: ")

#Arama butonu
b = Button(window, text="ARA", width=10,  command=get_data)
b.pack()

window.mainloop()
