# DOP
from operator import truediv


class Auto:
    kerekek = 4
    def __init__(self, marka, tipus = "nincs"):
        self.marka = marka
        self.tipus = tipus

class Téglalap:
    szog = 90
    def __init__(self, a_oldal = 5, b_oldal = 10):
        self.a_oldal = a_oldal
        self.b_oldal = b_oldal

    def terulet(self):
        return self.a_oldal * self.b_oldal

    def kerulet(self):
        return self.a_oldal * 2 + self.b_oldal * 2

class Dolgozo:
    ceg = "Minta Kft."
    def __init__(self, nev, kor, email, jelszo=""):
        self.nev = nev
        self.kor = kor
        self.email = email
        self.jelszo = jelszo

    def korkerdes(self):
        kor = input(f"Hány éves vagy {self.nev}:")
        self.kor = kor
        hiba = True
        for i in range(len(kor)):
            if kor[i].isnumeric():
                hiba = False
                break
        if hiba:
            print("Nem számjegyet adtál meg!")
            self.kor = 0
        else:
            self.kor = kor
        return

#---------------------------------------------------------
d = Dolgozo(3, 9)
print(d.kor)

t = Téglalap(3, 9)
print(t.a_oldal, t.b_oldal)
print(t.terulet())
print(t.kerulet())



a1 = Auto("Peugeot", "Partner")
a2 = Auto("Chery", "Tiggo")

# a1.kerekek = 3

print(a1.kerekek, a2.kerekek, Auto.kerekek)
print(a1.marka, a1.tipus)
print(a2.marka, a2.tipus)
