import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from mm_tarsasmodul import MMTarsasTar, mm_ido_formazasa


class MMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Társasjáték-napló")
        self.geometry("850x620")
        self.minsize(710, 540)
        self.tar = MMTarsasTar()

        ttk.Label(self, text="Társasjáték-napló", font=("Arial", 19, "bold")).pack(pady=(16, 3))
        ttk.Label(self, text="Játékaid, játékalkalmaid és statisztikáid egy helyen").pack(pady=(0, 12))

        self.fulek = ttk.Notebook(self)
        self.fulek.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.jatekok_ful = ttk.Frame(self.fulek, padding=14)
        self.statisztika_ful = ttk.Frame(self.fulek, padding=14)
        self.fulek.add(self.jatekok_ful, text="Játékok és naplózás")
        self.fulek.add(self.statisztika_ful, text="Statisztika")

        ttk.Label(self.jatekok_ful, text="A társasjátékaim", font=("Arial", 12, "bold")).pack(anchor="w")
        jatek_keret = ttk.Frame(self.jatekok_ful)
        jatek_keret.pack(fill="both", expand=True, pady=(8, 10))
        self.jatek_lista = ttk.Treeview(jatek_keret, columns=("nev",), show="headings", selectmode="browse")
        self.jatek_lista.heading("nev", text="Társasjáték neve")
        self.jatek_lista.column("nev", width=500, anchor="w")
        self.jatek_lista.pack(side="left", fill="both", expand=True)
        jatek_gorgeto = ttk.Scrollbar(jatek_keret, orient="vertical", command=self.jatek_lista.yview)
        jatek_gorgeto.pack(side="right", fill="y")
        self.jatek_lista.configure(yscrollcommand=jatek_gorgeto.set)
        self.jatek_lista.bind("<<TreeviewSelect>>", self.mm_kivalasztas)

        gombok = ttk.Frame(self.jatekok_ful)
        gombok.pack(fill="x", pady=(0, 16))
        ttk.Button(gombok, text="Új játék felvétele", command=self.mm_uj_jatek).pack(side="left", padx=(0, 8))
        ttk.Button(gombok, text="Átnevezés", command=self.mm_atnevezes).pack(side="left", padx=(0, 8))
        ttk.Button(gombok, text="Törlés", command=self.mm_torles).pack(side="left")

        naplo = ttk.LabelFrame(self.jatekok_ful, text="Új játékalkalom rögzítése", padding=12)
        naplo.pack(fill="x")
        self.kivalasztott_szoveg = tk.StringVar(value="Választott játék: nincs")
        ttk.Label(naplo, textvariable=self.kivalasztott_szoveg).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        ttk.Label(naplo, text="Ennyi percet játszottunk:").grid(row=1, column=0, sticky="w", padx=(0, 10))
        self.perc_szoveg = tk.StringVar(value="60")
        ttk.Entry(naplo, textvariable=self.perc_szoveg, width=10).grid(row=1, column=1, sticky="w")
        ttk.Button(naplo, text="Alkalom mentése", command=self.mm_alkalom_mentese).grid(row=1, column=2, sticky="w", padx=(18, 0))

        ttk.Label(self.statisztika_ful, text="Játékidő és alkalmak játékonként", font=("Arial", 12, "bold")).pack(anchor="w")
        self.statisztika_lista = ttk.Treeview(
            self.statisztika_ful,
            columns=("nev", "alkalmak", "osszes", "atlag"),
            show="headings", height=9
        )
        fejlecek = (
            ("nev", "Társasjáték", 240),
            ("alkalmak", "Alkalmak", 90),
            ("osszes", "Összes játékidő", 155),
            ("atlag", "Átlagos idő", 135),
        )
        for oszlop, fejlec, szelesseg in fejlecek:
            self.statisztika_lista.heading(oszlop, text=fejlec)
            self.statisztika_lista.column(oszlop, width=szelesseg, anchor="w")
        self.statisztika_lista.pack(fill="both", expand=True, pady=(8, 8))

        self.osszesito = tk.StringVar()
        ttk.Label(self.statisztika_ful, textvariable=self.osszesito, font=("Arial", 10, "bold")).pack(anchor="w", pady=(0, 16))
        ttk.Label(self.statisztika_ful, text="Legutóbbi játékalkalmak", font=("Arial", 12, "bold")).pack(anchor="w")
        self.elmenyek_lista = ttk.Treeview(
            self.statisztika_ful, columns=("datum", "jatek", "perc"), show="headings", height=6
        )
        for oszlop, fejlec, szelesseg in (
            ("datum", "Dátum", 175),
            ("jatek", "Társasjáték", 350),
            ("perc", "Játékidő", 125),
        ):
            self.elmenyek_lista.heading(oszlop, text=fejlec)
            self.elmenyek_lista.column(oszlop, width=szelesseg, anchor="w")
        self.elmenyek_lista.pack(fill="both", expand=True, pady=(8, 0))
        self.fulek.bind("<<NotebookTabChanged>>", self.mm_fulvaltas)
        self.mm_frissites()

    def mm_kivalasztott_jatek(self):
        kivalasztas = self.jatek_lista.selection()
        return kivalasztas[0] if kivalasztas else None

    def mm_kivalasztas(self, esemeny=None):
        nev = self.mm_kivalasztott_jatek()
        self.kivalasztott_szoveg.set(f"Választott játék: {nev or 'nincs'}")

    def mm_hiba(self, hiba):
        messagebox.showerror("Hiba", str(hiba), parent=self)

    def mm_uj_jatek(self):
        nev = simpledialog.askstring("Új társasjáték", "Mi a társasjáték neve?", parent=self)
        if nev is None:
            return
        try:
            self.tar.mm_uj_jatek(nev)
            self.mm_frissites(nev=" ".join(nev.split()))
        except (ValueError, OSError) as hiba:
            self.mm_hiba(hiba)

    def mm_atnevezes(self):
        regi = self.mm_kivalasztott_jatek()
        if not regi:
            messagebox.showwarning("Nincs kijelölés", "Előbb válassz ki egy játékot!", parent=self)
            return
        uj = simpledialog.askstring("Átnevezés", "Új név:", initialvalue=regi, parent=self)
        if uj is None:
            return
        try:
            self.tar.mm_atnevezes(regi, uj)
            self.mm_frissites(nev=" ".join(uj.split()))
        except (ValueError, OSError) as hiba:
            self.mm_hiba(hiba)

    def mm_torles(self):
        nev = self.mm_kivalasztott_jatek()
        if not nev:
            messagebox.showwarning("Nincs kijelölés", "Előbb válassz ki egy játékot!", parent=self)
            return
        if not messagebox.askyesno(
            "Törlés megerősítése",
            f"Törlöd ezt a játékot: {nev}?\nA hozzá tartozó játékalkalmak is törlődnek!",
            parent=self,
        ):
            return
        try:
            self.tar.mm_jatek_torlese(nev)
            self.mm_frissites()
        except (ValueError, OSError) as hiba:
            self.mm_hiba(hiba)

    def mm_alkalom_mentese(self):
        nev = self.mm_kivalasztott_jatek()
        if not nev:
            messagebox.showwarning("Nincs kijelölés", "Előbb válassz ki egy játékot!", parent=self)
            return
        try:
            perc = int(self.perc_szoveg.get())
            self.tar.mm_alkalom_rogzitese(nev, perc)
            self.mm_frissites(nev=nev)
            messagebox.showinfo("Mentve", f"{nev}: {mm_ido_formazasa(perc)} rögzítve.", parent=self)
        except (ValueError, OSError) as hiba:
            self.mm_hiba(hiba)

    def mm_fulvaltas(self, esemeny=None):
        if self.fulek.select() == str(self.statisztika_ful):
            self.mm_statisztika_frissites()

    def mm_frissites(self, nev=None):
        if nev is None:
            nev = self.mm_kivalasztott_jatek()
        for elem in self.jatek_lista.get_children():
            self.jatek_lista.delete(elem)
        for jatek in self.tar.mm_jatekok():
            self.jatek_lista.insert("", "end", iid=jatek, values=(jatek,))
        if nev in self.tar.mm_jatekok():
            self.jatek_lista.selection_set(nev)
            self.jatek_lista.focus(nev)
            self.jatek_lista.see(nev)
        self.mm_kivalasztas()
        self.mm_statisztika_frissites()

    def mm_statisztika_frissites(self):
        for lista in (self.statisztika_lista, self.elmenyek_lista):
            for elem in lista.get_children():
                lista.delete(elem)
        adatok = self.tar.mm_statisztika()
        for nev, darab, perc, atlag in adatok:
            self.statisztika_lista.insert(
                "", "end", values=(nev, darab, mm_ido_formazasa(perc), mm_ido_formazasa(atlag))
            )
        osszes_alkalom = sum(sor[1] for sor in adatok)
        osszes_perc = sum(sor[2] for sor in adatok)
        self.osszesito.set(
            f"Összesen: {len(adatok)} játék | {osszes_alkalom} alkalom | {mm_ido_formazasa(osszes_perc)}"
        )
        for alkalom in self.tar.mm_utolso_alkalmak():
            self.elmenyek_lista.insert(
                "", "end", values=(alkalom["datum"], alkalom["jatek"], mm_ido_formazasa(alkalom["perc"]))
            )


if __name__ == "__main__":
    app = MMApp()
    app.mainloop()
