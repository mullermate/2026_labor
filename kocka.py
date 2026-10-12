import tkinter as tk
from tkinter import ttk
import random

def dobas():
    szam = random.randint(1, 6)
    dobas_eredmenye.config(text=szam)

root = tk.Tk()
root.title("Kockázás")
root.geometry("600x400")
#root.minsize(500, 300)
#root.maxsize(800, 500)
#root.resizable(False, False)

cim_cimke = ttk.Label(text='Kockajáték',font='Arial 16 bold')
cim_cimke.grid(row=0, column=1, padx=10, pady=10)

dobas_szam = tk.StringVar(value="10")
dobas_szam_be = ttk.Entry(textvariable=dobas_szam, width=10)
dobas_szam_be.grid(row=1, column=0, padx=70, pady=10)

dobas_gomb = ttk.Button(root, text='Dobás', command=dobas)
dobas_gomb.grid(row=1, column=2, padx=10, pady=10)

kilepes_gomb = ttk.Button(root, text='Kilépés', command=root.destroy)
kilepes_gomb.grid(row=1, column=3, padx=10, pady=10)

dobas_eredmenye = ttk.Label(root, text='Eredmény', font='Arial 16 bold')
dobas_eredmenye.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
