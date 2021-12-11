import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
from time import strftime
from tkinter import messagebox
from tkinter import *

todos = {}

def detailTodo(cb=None):
    win = tk.Toplevel()
    win.wm_title('Detail kegiatan')
    selectedItem = treev.focus()
    selectedIndex = treev.item(selectedItem)['text'] #text adalah index dari kegiatan yang kita simpan
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value=selectedTodo['judul'])
    tk.Label(win, text='Tanggal:').grid(row=0, column=0, sticky='N')
    tk.Label(win, text='{} | {}'.format(tanggal, selectedTodo['waktu'])).grid(row=0, column=1, sticky='E')
    tk.Label(win, text='Judul:').grid(row=1, column=0, sticky='N')
    tk.Entry(win, state='disabled', textvariable=judul).grid(row=1, column=1, sticky='E')
    tk.Label(win, text='Keterangan:').grid(row=2, column=0, sticky='N')
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, sticky='E')
    keterangan.insert(tk.INSERT, selectedTodo['keterangan'])
    keterangan.configure(state='disabled', bg="#7FFFD4")    

def saveTodo():
    f = open('MyTodo.txt','w')
    f.write(str(todos))
    f.close()

def loadTodo():
    global todos
    f = open('MyTodo.txt','r')
    data = f.read()
    f.close()
    todos = eval(data) #dengan eval, data yang string diterjemahkan menjadi dict
    ListTodo()
    
def popupdel():
    response = messagebox.askquestion("Pemberitahuan!","Apakah anda ingin menghapusnya?")
    if response == "yes":
        selectedItem = treev.focus()
        tanggal = str(cal.selection_get())
        todos[tanggal].pop(treev.item(selectedItem)["text"])
        ListTodo()  

"""
def delTodo():
    tanggal = str(cal.selection_get())
    selectedItem = treev.focus() #akan mendapatkan index dari item yang diklik di treeview
    todos[tanggal].pop(treev.item(selectedItem)['text'])
    ListTodo()
#pop berguna untuk menghapus item
"""
    
def ListTodo(cb=None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert('','end', text=i, values=(todos[tanggal][i]['judul'], todos[tanggal][i]['waktu']))


def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        'waktu':'{}:{}'.format(jam.get(), menit.get()),
        'judul': judul.get(),
        'keterangan': keterangan.get('1.0', tk.END) #mengambil keterangan dari line pertama sampai line terakhir
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()

def AddForm():
    win = tk.Toplevel()
    win.wm_title('+')
    jam = tk.IntVar(value=10) #Jam merupakan integer
    menit = tk.IntVar(value=30)
    judul = tk.StringVar(value='')
    tk.Label(win, text='Waktu: ', font="Garamond 12").grid(row=0, column=0)
    tk.Spinbox(win, from_=0, to=23, textvariable=jam, font="Garamond 12",
            width=3, bg="#C32148", fg="white").grid(row=0, column=1)
    tk.Spinbox(win, from_=0, to=59, textvariable=menit, font="Garamond 12",
            width=3, bg="#FF007F", fg="white").grid(row=0, column=2)
    tk.Label(win, text='Judul: ', font="Garamond 12").grid(row=1, column=0)
    tk.Entry(win, textvariable=judul, font="Garamond 12", 
            bg="#E7FEFF").grid(row=1, column=1, columnspan=2)
    tk.Label(win, text='Keterengan', font="Garamond 12").grid(row=2, column=0)
    keterangan = ScrolledText(win, width=12, height=5, font="Garamond 12",
                            bg="#89CFF0")
    keterangan.grid(row=2, column=1, columnspan=2, rowspan=4)
    tanggal = str(cal.selection_get())
    tk.Button(win, text='Tambah', font="Garamond 12", command = lambda: addTodo(win, tanggal, jam, 
            menit, judul, keterangan), bg="#013220", fg="white").grid(row=6, column=1)


def title():
  #  global cal
    waktu = strftime('%H:%M')
    tanggal = str(cal.selection_get())
    root.title(tanggal + " | " + waktu + " | Calendar Fadhel's")
    root.after(1000,title)

root = tk.Tk()
root.title('Kalenderku')
root.configure(background="#A3C1AD")
style = ttk.Style(root)
style.theme_use("clam")
style.configure('Treeview', font="Garamond 11", rowheight=16, fieldbackground="#EDC9AF")

my_menu=Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=saveTodo)
file_menu.add_command(label="Load", command=loadTodo)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Tambah", command=AddForm)
edit_menu.add_command(label="Hapus", command=popupdel)

cal = Calendar(root, font='Broadway 16', selectmode='day', locale='id_ID', cursor='pirate')
cal.pack(pady=20, fill="both", expand=True)
cal.grid(row=0, column=3, sticky='WNE', rowspan=7)
cal.bind('<<CalendarSelected>>', ListTodo) #Jika memilih tanggal yang berbeda, akan memanggil ListTodo
cal.configure(background="#FF6961", foreground="#FFB7C5", bordercolor="white", borderwidth=6,
            normalbackground="#FF6961", normalforeground="#FFB7C5",
            headersbackground="#FFB7C5", headersforeground="#FF6961", 
            selectbackground="#FFB7C5", selectforeground="#FF6961",
            othermonthbackground="#DE5D83", othermonthforeground="#E7FEFF", weekendbackground="#CD5C5C",
            weekendforeground="white", othermonthwebackground="#DE3163",
            othermonthweforeground="#E7FEFF", showweeknumbers=False)

tanggal = str(cal.selection_get())

treev = ttk.Treeview(root)
treev.grid(row=0, column=0, sticky='WNE', rowspan=4, columnspan=2)
scrollBar = tk.Scrollbar(root, orient='vertical', command=treev.yview)
#artinya, scrollbar yang dibuat disini berfyungsi untuk mengatur posisi y (vertikal)
#atau atas bawah, seperti sb.y pada diagram kartesius
scrollBar.grid(row=0, column=2, sticky='ENS', rowspan=4)
#ens untuk memposisikan di pojok kanan dan ada di treeview

treev.configure(yscrollcommand=scrollBar.set)
treev.bind('<Double-1>', detailTodo) #membinding tombol klik kiri sebanyak 2 kali (double klik) dan memanggil detail todo
treev['columns'] = ('1', '2')
treev['show'] = 'headings'
treev.column('2', width=100)
treev.heading('2', text='JAM')
treev.heading('1', text='Judul')


#Adding button
btnAdd = tk.Button(root, text='Tambah', width=16, command=AddForm, font="Broadway 11", 
                bg="#E52B50", fg="white")
btnAdd.grid(row=4, column=0, sticky='N')

btnDel = tk.Button(root, text='Hapus', width=16, command=popupdel, font="Broadway 11", 
                bg="#FFEF00")
btnDel.grid(row=6, column=0, sticky='N')

btnLoad = tk.Button(root, text='Load', width=16, command=loadTodo, font="Broadway 11",
                bg="#A4C639", fg="white")
btnLoad.grid(row=6, column=1, sticky='N')

btnSave = tk.Button(root, text='Save', width=16, command=saveTodo, font="Broadway 11",
                bg="#318CE7")
btnSave.grid(row=4, column=1, sticky='N')

title()
root.mainloop()
