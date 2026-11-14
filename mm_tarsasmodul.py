import json
from datetime import datetime
from pathlib import Path


def mm_adatok_betoltese(utvonal):
    if not utvonal.exists():
        return {"jatekok": [], "alkalmak": []}
    with utvonal.open("r", encoding="utf-8") as fajl:
        adatok = json.load(fajl)
    if not isinstance(adatok, dict):
        raise ValueError("A mentett adatok formátuma hibás.")
    if not isinstance(adatok.get("jatekok"), list) or not isinstance(adatok.get("alkalmak"), list):
        raise ValueError("A mentett adatokból hiányzik egy szükséges lista.")
    if not all(isinstance(nev, str) for nev in adatok["jatekok"]):
        raise ValueError("A társasjátékok listája hibás.")
    if not all(
        isinstance(alkalom, dict)
        and isinstance(alkalom.get("jatek"), str)
        and isinstance(alkalom.get("perc"), int)
        and isinstance(alkalom.get("datum"), str)
        for alkalom in adatok["alkalmak"]
    ):
        raise ValueError("A mentett játékalkalmak formátuma hibás.")
    return adatok


def mm_adatok_mentese(utvonal, adatok):
    atmeneti = utvonal.with_suffix(".tmp")
    with atmeneti.open("w", encoding="utf-8") as fajl:
        json.dump(adatok, fajl, ensure_ascii=False, indent=2)
    atmeneti.replace(utvonal)


def mm_ido_formazasa(percek):
    ora, perc = divmod(percek, 60)
    if ora == 0:
        return f"{perc} perc"
    if perc == 0:
        return f"{ora} óra"
    return f"{ora} óra {perc} perc"


class MMTarsasTar:
    def __init__(self, utvonal=None):
        self.utvonal = Path(utvonal) if utvonal else Path.home() / "tarsasjatekok_mm_adatok.json"
        self.adatok = mm_adatok_betoltese(self.utvonal)

    def mm_jatekok(self):
        return sorted(self.adatok["jatekok"], key=str.casefold)

    def mm_uj_jatek(self, nev):
        nev = " ".join(nev.split())
        if not nev:
            raise ValueError("Add meg a társasjáték nevét!")
        if len(nev) > 80:
            raise ValueError("A név legfeljebb 80 karakter lehet.")
        if any(regi.casefold() == nev.casefold() for regi in self.adatok["jatekok"]):
            raise ValueError("Ez a társasjáték már szerepel a listában.")
        self.adatok["jatekok"].append(nev)
        mm_adatok_mentese(self.utvonal, self.adatok)

    def mm_atnevezes(self, regi, uj):
        uj = " ".join(uj.split())
        if not uj or len(uj) > 80:
            raise ValueError("Az új név 1–80 karakterből álljon.")
        if any(nev.casefold() == uj.casefold() and nev != regi for nev in self.adatok["jatekok"]):
            raise ValueError("Ilyen nevű társasjáték már létezik.")
        hely = self.adatok["jatekok"].index(regi)
        self.adatok["jatekok"][hely] = uj
        for alkalom in self.adatok["alkalmak"]:
            if alkalom["jatek"] == regi:
                alkalom["jatek"] = uj
        mm_adatok_mentese(self.utvonal, self.adatok)

    def mm_jatek_torlese(self, nev):
        self.adatok["jatekok"].remove(nev)
        self.adatok["alkalmak"] = [
            alkalom for alkalom in self.adatok["alkalmak"] if alkalom["jatek"] != nev
        ]
        mm_adatok_mentese(self.utvonal, self.adatok)

    def mm_alkalom_rogzitese(self, nev, perc):
        if nev not in self.adatok["jatekok"]:
            raise ValueError("Válassz ki egy társasjátékot!")
        if not isinstance(perc, int) or not 1 <= perc <= 1440:
            raise ValueError("A játékidő 1 és 1440 perc között lehet.")
        self.adatok["alkalmak"].append({
            "jatek": nev,
            "perc": perc,
            "datum": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        mm_adatok_mentese(self.utvonal, self.adatok)

    def mm_statisztika(self):
        eredmeny = []
        for nev in self.mm_jatekok():
            idok = [alkalom["perc"] for alkalom in self.adatok["alkalmak"] if alkalom["jatek"] == nev]
            darab = len(idok)
            osszes = sum(idok)
            atlag = round(osszes / darab) if darab else 0
            eredmeny.append((nev, darab, osszes, atlag))
        return eredmeny

    def mm_utolso_alkalmak(self, darab=10):
        return list(reversed(self.adatok["alkalmak"][-darab:]))
