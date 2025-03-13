import random
from Consts import *


class DataSet:
    def __init__(self):
        self.klasy = 6  # liczba klas w szkole (klasa jako grupa uczniów)
        self.nauczyciele = 12  # liczba nauczycieli
        self.sale = 12  # liczba sal (sala jako pomieszczenie)
        self.zajecia = 12  # maksymalna liczba zajęc w dniu
        self.tydzien = self.zajecia * 5  # maksymalna liczba zajęc w tygodniu
        self.rozkladZajec = [5, 4, 3, 3, 2, 2, 2, 2, 1, 1, 0, 0]  # rozkład ile lekcji ma jakaś klasa z danym nauczycielem

        # tutaj inicjuje nasze dane czyli plan zajęć dla klas, nauczycieli i sal
        # OKIENKO bedzie tutaj oznaczać że w tym miejscu w planie nie ma żadnej lekcji wpisanej
        # używamy tutaj wektorów więc zeby sprawdzić jaką lekcje ma klasa 2 we wtorek na 3 lekcji trzeba
        # udać się do indeksu [(indeks_klasy-1)*tydzien+zajecia*(dzien_tyodnia-1)+lekcja_danego_dnia-1]
        # czyli w tym przypadku [1*40+8+2] = 50
        self.TablicaKlas = [OKIENKO for _ in range(5 * self.zajecia * self.klasy)]
        self.TablicaSali = [OKIENKO for _ in range(5 * self.zajecia * self.sale)]
        self.TablicaNauczycieli = [OKIENKO for _ in range(5 * self.zajecia * self.nauczyciele)]

    def SetZajecia(self, klasa, nauczyciel, sala, dzien_tygodnia, lekcja):  # ustawia element planu dla każdej listy
        if (dzien_tygodnia != None):
            self.TablicaKlas[(klasa) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (nauczyciel, sala)
            self.TablicaNauczycieli[(nauczyciel) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (
            klasa, sala)
            self.TablicaSali[(sala) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (klasa, nauczyciel)
        else:
            self.TablicaKlas[(klasa) * self.tydzien + lekcja] = (nauczyciel, sala)
            self.TablicaNauczycieli[(nauczyciel) * self.tydzien + lekcja] = (klasa, sala)
            self.TablicaSali[(sala) * self.tydzien + lekcja] = (klasa, nauczyciel)

    def GetZajecia(self, czyj_plan, indeks, dzien_tygodnia, lekcja):  # zwraca komórkę z danej tablicy, wszystkie parametry indeksowane od zera
        if czyj_plan == KLASA:
            tablica = self.TablicaKlas
        elif czyj_plan == NAUCZYCIEL:
            tablica = self.TablicaNauczycieli
        else:
            tablica = self.TablicaSali
        if dzien_tygodnia != None:
            return tablica[(indeks) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja]
        else:
            return tablica[(indeks) * self.tydzien + lekcja]  # jeżeli nie podamy dnia tygodnia to można bezpośrednio id zajęcia względem początku tygodnia (np. lekcja == 9 zwróci nam drugą lekcję wtorku)


    def GetDzien(self, czyj_plan, indeks, dzien_tygodnia):  # zwraca listę komorek z calego dnia z danej tablicy , wszystkie parametry indeksowane od zera
        if czyj_plan == KLASA:
            tablica = self.TablicaKlas
        elif czyj_plan == NAUCZYCIEL:
            tablica = self.TablicaNauczycieli
        else:
            tablica = self.TablicaSali
        return [tablica[(indeks) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] for lekcja in range(self.zajecia)]

    def GetTydzien(self, czyj_plan,
                   indeks):  # zwraca listę komorek z calego tygodnia z danej tablicy , wszystkie parametry indeksowane od zera
        if czyj_plan == KLASA:
            tablica = self.TablicaKlas
        elif czyj_plan == NAUCZYCIEL:
            tablica = self.TablicaNauczycieli
        else:
            tablica = self.TablicaSali

        return [tablica[(indeks) * self.tydzien + self.zajecia * (dzien) + lekcja] for dzien in range(DNI_TYGODNIA) for
                lekcja in range(self.zajecia)]

    def GenerujPlan(self):
        """
        Losowo generuje początkowy plan dla każdej klasy,nauczyciela i sali.
        To ile zajęć ma klasa z danym nauczycielem określa wektor rozkladZajęć i jego
        przesunięcie np klasa 2 ma przesunięty ten wektor o 2 w prawy czyli ma 5 zajęc z nauczycielem
        o indeksie 2 (dla ułatwienia poźniejszych odniesień do indeksów indeksy klas, sal i nauczycieli
        są indeksowane od 0!!!).
        :return:
        """

        for i in range(self.klasy):  # pętla po każdej z klas
            offset = self.tydzien * i  # offset w tablicyklas
            for j in range(len(self.rozkladZajec)):  # pętla dla każdego nauczyciela
                if i + j >= len(self.rozkladZajec):  # wybieramy ile zajęc bedzie
                    nauczyciel = i + j - len(
                        self.rozkladZajec)  # miala klasa z danym nauczycielem (indeks z rozkładZajec)
                else:
                    nauczyciel = j + i
                for _ in range(self.rozkladZajec[nauczyciel]):  # pętla która dla nauczyliela i klasy ustala
                    timeAccept = False  # termin i sale w której sie odbywa lekcja
                    roomAccept = False
                    time = None
                    room = None
                    while (not timeAccept):  # tutaj w ifie sprawdzam czy klasa i nauczyciel mają tutaj wolne
                        time = random.randint(0, self.tydzien - 1)
                        if (self.TablicaKlas[time + offset] == OKIENKO and self.TablicaNauczycieli[j * self.tydzien + time] == OKIENKO):
                            timeAccept = True
                    while (not roomAccept):  # tutaj sprawdzam czy sala wylosowana jest wolna
                        room = random.randint(0, self.sale - 1)
                        if self.TablicaSali[room * self.tydzien + time] == OKIENKO:
                            roomAccept = True

                    self.TablicaKlas[time + offset] = (j, room)  # w tych liniach i to indeks klasy, j nauczyciela, room sali
                    self.TablicaNauczycieli[j * self.tydzien + time] = (i, room)
                    self.TablicaSali[room * self.tydzien + time] = (i, j)


    def WypiszPlan(self):
        """
        Wypisywanie planu danej klasy w celu debugowania. \n
        Każda linijka to jeden dzien dla danej klasy. \n
        Plan każdej klasy jest oddzielony od innych endl. \n
        :return:
        """
        for i in range(len(self.TablicaKlas)):
            if i%self.tydzien == self.tydzien-1:
                print(self.TablicaKlas[i])
                print('\n')
            elif i%self.zajecia ==self.zajecia-1:
                print(self.TablicaKlas[i])
            else:
                print(self.TablicaKlas[i],end=' ')

    def Count_bloki(self, dzien):  # zlicza bloki lekcyjne podanego dnia
        bloki = 0
        is_in_blok = False  # True jeżeli lekcja jest w srodku bloku
        for lekcja in range(len(dzien)):
            if dzien[lekcja][0] != -1 and is_in_blok == False:
                bloki += 1
                is_in_blok = True

            elif dzien[lekcja][0] == -1 and is_in_blok == True:  # czy koniec bloku zajec
                is_in_blok = False

        return bloki

    def Count_bloki_przedmiotowe_d_godzinne(self, dzien,
                                            d):  # zlicza ile bloków d-godzinnych tej samej pary nauczyciel+klasa+sala
        bloki_p = 0  # POTENTIAL ISSUE - ten algorytm zidentyfikuje jeden blok 2d-godzinny jako dwa bloki, można zniwelować to w fitnessach dając kary za bloki o wysokich d
        current_pair = (-1, -1)  # aktuana para nauczyciel-sala
        current_length = 0
        for lekcja in range(len(dzien)):

            if dzien[lekcja] == current_pair and dzien[lekcja] != OKIENKO:
                current_length += 1
                if current_length == d - 1:
                    bloki_p += 1
                    current_length = 0
                    current_pair = (-1, -1)
            else:
                current_pair = dzien[lekcja]
        return bloki_p

    def Czy_dzien_wolny(self, dzien):  # True jeżeli klasa ma nie ma lekcji tego dnia
        for lekcja in range(len(dzien)):
            if [lekcja][0] != -1:
                return False
        return True

    def Premia_za_ilosc_godzin(self, dzien, min, max):  # zwraca true jeżeli ilość godzin w dniu należy do przedziału [min,max] włącznie
        count = 0
        for lekcja in range(len(dzien)):
            if [lekcja][0] != -1:
                count += 1
                if count > max:
                    return False
        if count < min:
            return False
        return True

    def Ocen_godziny(self, dzien, godziny_values):
        przyjazne_godziny_score = 0
        for lekcja in range(len(dzien)):
            if dzien[lekcja][0] != -1:
                przyjazne_godziny_score += godziny_values[lekcja]
        return przyjazne_godziny_score

    def Simple_fitness(self):  # patrzymy tylko na to ile bloków zajęć mają łącznie klasy i w jakich godzinach mają zajęcia
        godziny_values = [i * 2 for i in range(self.zajecia // 2)] + [(self.zajecia - i) for i in range(self.zajecia // 2)]  # sample [0, 2, 4, 6, 8, 7, 6, 5] im więcej tym lepsza godzina
        bloki = 0
        przyjazne_godziny_score = 0
        for id_klasy in range(self.klasy):
            for dzien_tygodnia in range(DNI_TYGODNIA):
                dzien = self.GetDzien(KLASA, id_klasy, dzien_tygodnia)
                bloki += self.Count_bloki(dzien)
                przyjazne_godziny_score += self.Ocen_godziny(dzien, godziny_values)

        fitness = przyjazne_godziny_score - bloki * 10
        return fitness

    def Better_fitness(self):
        godziny_values = [i * 2 for i in range(self.zajecia // 2)] + [(self.zajecia - i) for i in
                                                                      range(self.zajecia // 2)]
        bloki = 0
        premia_za_rozkład_godzinny = 0
        przyjazne_godziny_score = 0
        dni_wolne = 0
        bloki_przedmiotowe = 0
        for id_klasy in range(self.klasy):
            for dzien_tygodnia in range(DNI_TYGODNIA):
                dzien = self.GetDzien(KLASA, id_klasy, dzien_tygodnia)
                bloki += self.Count_bloki(dzien)
                premia_za_rozkład_godzinny += self.Premia_za_ilosc_godzin(dzien, 4, 6)
                przyjazne_godziny_score += self.Ocen_godziny(dzien, godziny_values)
                dni_wolne += self.Czy_dzien_wolny(dzien)
                bloki_przedmiotowe += self.Count_bloki_przedmiotowe_d_godzinne(dzien, 2)

        # print(premia_za_rozkład_godzinny*5, przyjazne_godziny_score//5,  dni_wolne*100, bloki_przedmiotowe*100, bloki*2) - za duzo blokow
        # fitness = premia_za_rozkład_godzinny * 5 + przyjazne_godziny_score // 5 + dni_wolne * 100 + bloki_przedmiotowe * 100 - bloki * 2
        fitness = premia_za_rozkład_godzinny * 5 + przyjazne_godziny_score // 3 + dni_wolne * 100 + bloki_przedmiotowe * 5 - bloki * 3
        # print(fitness)
        return fitness

    def Evaluate(self, param):
        if param == SIMPLE:
            return self.Simple_fitness()
        elif param == BETTER:
            return self.Better_fitness()

    def Get_free_rooms(self, dzien, lekcja):  # zwraca listę sali które są wolne w podanym terminie
        wolne_sale = []
        for i in range(self.sale):
            if self.GetZajecia(SALA, i, dzien, lekcja) == OKIENKO:
                wolne_sale.append(i)
        return wolne_sale

    def Get_wspolne_okienka(self, nauczyciel, klasa):  # zwraca listę wolnych terminów dla klasy i nauczycieli NIE PATRZAC NA SALE
        wspolne_okienka = []
        terminy_nauczyciel = self.GetTydzien(NAUCZYCIEL, nauczyciel)
        terminy_klasa = self.GetTydzien(KLASA, klasa)
        for i in range(self.tydzien):
            if terminy_nauczyciel[i] == OKIENKO and terminy_klasa[i] == OKIENKO:
                wspolne_okienka.append(i)
        return wspolne_okienka

    def Wstaw_okienko(self, klasa, nauczyciel, sala, dzien_tygodnia, lekcja):
        if (dzien_tygodnia != None):
            self.TablicaKlas[(klasa) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (-1, -1)
            self.TablicaNauczycieli[(nauczyciel) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (
                -1, -1)
            self.TablicaSali[(sala) * self.tydzien + self.zajecia * (dzien_tygodnia) + lekcja] = (-1, -1)
        else:
            self.TablicaKlas[(klasa) * self.tydzien + lekcja] = (-1, -1)
            self.TablicaNauczycieli[(nauczyciel) * self.tydzien + lekcja] = (-1, -1)
            self.TablicaSali[(sala) * self.tydzien + lekcja] = (-1, -1)

    def Basic_random_swap(self):  # zamieni miejscami dwa terminy jednej klasie, sale pozostają w danym dniu i godzinie
        klasa = random.randint(0, self.klasy - 1)
        wspolne_okienka = []
        while (True):
            lekcja_id = random.randint(0, self.tydzien - 1)
            termin1 = self.GetZajecia(KLASA, klasa, None, lekcja_id)
            if termin1 == OKIENKO:
                continue
            wspolne_okienka = self.Get_wspolne_okienka(termin1[0], klasa)
            if len(wspolne_okienka) <= 0:
                continue
            lekcja2_id = wspolne_okienka[random.randint(0, len(wspolne_okienka) - 1)]
            wolne_sale = self.Get_free_rooms(None, lekcja2_id)
            if len(wolne_sale) > 0:
                break

        termin2 = self.GetZajecia(KLASA, klasa, None, lekcja2_id)

        if termin2 == OKIENKO:
            termin2 = (termin2[0], wolne_sale[random.randint(0, len(wolne_sale) - 1)])
            termin1 = (termin1[0], -1)

        self.SetZajecia(klasa, termin1[0], termin2[1], None, lekcja2_id)
        self.SetZajecia(klasa, termin2[0], termin1[1], None, lekcja_id)
        # print("Zamieniono terminy dla klasy: ", klasa, " lekcja1: ", lekcja_id, " lekcja2: ", lekcja2_id)

    def Random_Swap(self):
        klasa = random.randint(0, self.klasy - 1)
        zajecia = []
        okienka = []

        for i in range(self.tydzien):
            if self.GetZajecia(KLASA, klasa, None, i) == OKIENKO:
                okienka.append(i)
            else:
                zajecia.append(i)

        termin = random.choice(zajecia)
        instancja_terminu = self.GetZajecia(KLASA, klasa, None, termin)
        random.shuffle(okienka)

        for indeks_okienka in okienka:
            if (self.GetZajecia(NAUCZYCIEL, instancja_terminu[0], None, indeks_okienka) == OKIENKO and
                    self.GetZajecia(SALA, instancja_terminu[1], None, indeks_okienka) == OKIENKO and
                    indeks_okienka != termin):
                self.SetZajecia(klasa, instancja_terminu[0], instancja_terminu[1], None, indeks_okienka)
                self.Wstaw_okienko(klasa, instancja_terminu[0], instancja_terminu[1], None, termin)
                break

    def CheckForRoomCollisions(self):
        for lekcja in range(self.zajecia):
            for dzien in range(DNI_TYGODNIA):
                zajecia_w_salach = {}
                for klasa in range(self.klasy):
                    indeks = klasa * self.tydzien + dzien * self.zajecia + lekcja
                    nauczyciel, sala = self.TablicaKlas[indeks]
                    if sala != -1:  # Sprawdź, czy sala nie jest okienkiem
                        if sala not in zajecia_w_salach:
                            zajecia_w_salach[sala] = (klasa, nauczyciel)
                        else:
                            # Kolizja: ta sama sala jest już używana przez inną klasę
                            klasa1, nauczyciel1 = zajecia_w_salach[sala]
                            klasa2 = klasa
                            if klasa1 != klasa2:
                                print(f"Kolizja w sali {sala} w dniu {dzien} o godzinie {lekcja}: klasa {klasa1} i klasa {klasa2}")
                                return True
        return False

    def CountOkienka(self):
        """
        Zlicza okienka w planie zajęć dla każdej klasy.
        Wypisuje liczbę okienek dla każdej klasy.
        """

        for klasa in range(self.klasy):
            okienka = 0
            for dzien in range(DNI_TYGODNIA):
                for lekcja in range(self.zajecia):
                    if self.GetZajecia(KLASA, klasa, dzien, lekcja) == OKIENKO:
                        okienka += 1
            print(f"Klasa {klasa} ma {okienka} okienek")
            if okienka != 35:
                print("Klasa: ", klasa)
