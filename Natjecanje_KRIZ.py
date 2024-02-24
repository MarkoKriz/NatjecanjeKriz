#KEF (Kalkulator elektrodinamike za fiziku)

import math

ispravneOznake = {"U", "I", "R", "P", "W", "Q", "T"}

mjerneJedinice = {
    "U" : "V",
    "I" : "A",
    "R" : "Ohm",
    "P" : "W",
    "W" : "J",
    "Q" : "C",
    "T" : "s"
}

RcheckO = {"R"}

imenaVelicina = {
    "U": "napon",
    "I": "struja",
    "R": "otpor",
    "Q": "naboj",
    "W": "rad",
    "P": "snaga",
    "T": "vrijeme"
}

Ucheck = [({"I", "R"}, lambda vals : vals["I"] * vals["R"]), 
          ({"I", "P"}, lambda vals : vals["P"] / vals["I"]), 
          ({"R", "P"}, lambda vals : math.sqrt(vals["P"] * vals["R"])),
          ({"W", "T", "I"}, lambda vals : vals["W"] * vals["T"] / vals["I"]),
          ({"W", "T", "Q"}, lambda vals : vals["W"] * vals["T"] * vals["T"] / vals["Q"])]
Icheck = [({"U", "R"}, lambda vals : vals["U"] / vals["R"]),
          ({"R", "P"}, lambda vals : math.sqrt(vals["P"] / vals["R"] )),
          ({"U", "P"}, lambda vals : vals["P"] / vals["U"]),
          ({"Q", "T"}, lambda vals : vals["Q"] / vals["T"])]
Rcheck = [({"I", "U"}, lambda vals : vals["U"] / vals["I"]),
          ({"I", "P"}, lambda vals : vals["P"] / vals["I"] * vals["I"]),
          ({"U", "P"}, lambda vals : vals["U"] * vals["U"] / vals["P"])]
Pcheck = [({"U", "I"}, lambda vals : vals["U"] * vals["I"]),
          ({"I", "R"}, lambda vals : vals["I"] * vals["I"] * vals["R"]),
          ({"U", "R"}, lambda vals : vals["U"] * vals["U"] / vals["R"]),
          ({"W", "T"}, lambda vals : vals["W"] / vals["T"])]
Wcheck = [({"P", "T"}, lambda vals : vals["P"] * vals["T"]),
          ({"U", "Q"}, lambda vals : vals["U"] * vals["Q"])]
Qcheck = [({"I", "T"}, lambda vals : vals["I"] * vals["T"]),
          ({"U", "R", "T"}, lambda vals : (vals["U"] * vals["T"]) / vals["R"]),
          ({"P", "U", "T"}, lambda vals : vals["P"] / vals["U"] * vals["T"])]
Tcheck = [({"Q", "I"}, lambda vals : vals["Q"] / vals["I"]),
          ({"W", "P"}, lambda vals : vals["W"] / vals["P"]),
          ({"W", "U", "I"}, lambda vals : vals["W"] / (vals["U"] * vals["I"]))]

pravilaZaRacunanje = {
    "U" : Ucheck,
    "I" : Icheck,
    "R" : Rcheck,
    "P" : Pcheck,
    "W" : Wcheck,
    "Q" : Qcheck,
    "T" : Tcheck
}

def pitajKorisnikaZaOznake():
    print("")
    print("Dobar dan unesite oznake fizickih velicina koje imate.")
    print("Prihvacene su sljedece oznake :")
    for oznaka in ispravneOznake:
        print(f"    {oznaka} - {imenaVelicina[oznaka]} u [{mjerneJedinice[oznaka]}]")
    print("Za izlaz iz programa unesite X")
    unos = input("Vas unos : ").upper()
    return unos

def korisnickiUnosIspravan(unos):
    for oznaka in unos:
        if(oznaka not in ispravneOznake):
            return False
        
    return True

def zatrazenPrekidPrograma(unos):
    if "X" in unos:
        return True
    
    return False

def unosJeLogican(unos):
    unesene_oznake = set(unos)

    if len(unesene_oznake) == 0:
        return False

    for oznaka in unesene_oznake:
        for pravilo in pravilaZaRacunanje[oznaka]:
            if pravilo[0].issubset(unesene_oznake):
                print(f"{oznaka} se unosi i racuna, ponovi unos")
                return False

    return True

def pitajKorisnikaZaVrijenosti(unos):
    dict_oznaka_vrijednost = {}

    for oznaka in unos:
        if oznaka == "R":
            continue
        while(True):
            try:
                vrijednost = float(input(f"Unesi vrijednost {oznaka} u mjernoj jedinici [{mjerneJedinice[oznaka]}] : "))
                if(vrijednost <= 0.0):
                    raise
                dict_oznaka_vrijednost[oznaka] = vrijednost
                break
            except:
                print(f"Vrijednost {oznaka} mora biti pozitivan broj")

    return dict_oznaka_vrijednost

def praviloSeMozeIzracunati(pravilo, dostupne_vrijednosti):
    for oznaka in pravilo:
        if oznaka not in dostupne_vrijednosti:
            return False
    return True

def dohvatPravilaZaRacunanje(oznaka, dostupne_vrijednosti):
    dostupne_oznake = set(dostupne_vrijednosti.keys())

    for pravilo in pravilaZaRacunanje[oznaka]:
        if pravilo[0].issubset(dostupne_oznake):
            return pravilo


    

def rjesavanjeOtpornika():
    unos = ""
    while(unos != "d" and unos != "n"):
        unos = input("Imate li vise od jednog otpornika/trošila u sustavu : [d/n] ")

    jedanOtpornik = False if unos == "d" else True

    if jedanOtpornik:
        while(True):
            try:
                vrijednostOtpornika = float(input(f"Unesite vrijednost otpora u [ {mjerneJedinice['R']} ] :"))
                if(vrijednostOtpornika <= 0.0):
                    raise
                return {"R" : vrijednostOtpornika}
            except:
                print(f"Vrijednost otpora mora biti pozitivan broj")
        
    broj_otpornika = 0
    while(True):
        try:
            broj_otpornika = int(input("Koliko imate otponika/trošila : "))
            if broj_otpornika <= 1:
                raise 
            break
        except:
            print("Unos za broj otpornika/trošila mora biti cijeli broj veci od 1")
    
    unos = ""
    while(unos != "p" and unos != "s"):
        unos = input("Jesu li spojeni paralelno ili u seriji : [p/s] ")

    paralelniSpoj = True if unos == "p" else False

    ukupniOtpor = 0

    for i in range(broj_otpornika):
        vrijednostOtpornika = 0
        while(True):
            try:
                vrijednostOtpornika = float(input(f"Unsei vrijednost {i+1}. otpora u {mjerneJedinice['R']}: "))
                if vrijednostOtpornika < 0.0:
                    raise 
                break
            except:
                print("Unos za broj otpornika/trošila mora biti broj veci od 0.0")
        
        if paralelniSpoj:
            ukupniOtpor = ukupniOtpor + 1/vrijednostOtpornika
        else:
            ukupniOtpor = ukupniOtpor + vrijednostOtpornika

    if paralelniSpoj:
        ukupniOtpor = 1/ukupniOtpor
    
    return {"R" : ukupniOtpor}

    

def main():

    while(True):
        korisnicki_unos_oznake = pitajKorisnikaZaOznake()

        if (not korisnickiUnosIspravan(korisnicki_unos_oznake) and not zatrazenPrekidPrograma(korisnicki_unos_oznake)):
            print("Neispravan unos")
            continue
        elif zatrazenPrekidPrograma(korisnicki_unos_oznake):
            break

        if not unosJeLogican(korisnicki_unos_oznake):
            continue

        vrijednosti_velicina = {}

        if "R" in korisnicki_unos_oznake:
            vrijednosti_velicina.update(rjesavanjeOtpornika())        

        vrijednosti_velicina.update(pitajKorisnikaZaVrijenosti(korisnicki_unos_oznake))


        for oznaka in ispravneOznake:
            if oznaka not in vrijednosti_velicina.keys():
                pravilo = dohvatPravilaZaRacunanje(oznaka, vrijednosti_velicina)
                if pravilo is None:
                    continue
                print(f"{oznaka} se moze izracunati iz {pravilo[0]}")
                funkcijaZaIzracun = pravilo[1]
                print(f"{oznaka} = {funkcijaZaIzracun(vrijednosti_velicina)} [{mjerneJedinice[oznaka]}]")

    print("Izlaz iz programa")


main()
