import random
import matplotlib.pyplot as plt
from DataSet import DataSet
from Consts import *
import time

class GeneticAlgorithm:
    def __init__(self, populacja_rozmiar, pokolenia, prawdopodobienstwo_mutacji, n_elite, rodzaj_oceny):
        self.populacja_rozmiar = populacja_rozmiar
        self.pokolenia = pokolenia
        self.prawdopodobienstwo_mutacji = prawdopodobienstwo_mutacji
        self.n_elite = n_elite
        self.rodzaj_oceny = rodzaj_oceny
        self.population = self.initial_population()
        self.best_fitness_history = []
        self.times_to_reach_fitness = {800: None, 1000: None, 1200: None, 1230: None}
        self.generations_to_reach_fitness = {800: None, 1000: None, 1200: None, 1230: None}

    def initial_population(self):
        population = []
        for _ in range(self.populacja_rozmiar):
            ds = DataSet()
            ds.GenerujPlan()
            population.append(ds)
        return population

    def fitness(self, ds):
        if self.rodzaj_oceny == SIMPLE:
            return ds.Evaluate(SIMPLE)
        elif self.rodzaj_oceny == BETTER:
            return ds.Evaluate(BETTER)

    def population_best(self):
        best_individual = None
        best_individual_fitness = -1
        for individual in self.population:
            individual_fitness = self.fitness(individual)
            if individual_fitness > best_individual_fitness:
                best_individual = individual
                best_individual_fitness = individual_fitness
        return best_individual, best_individual_fitness

    def selekcja(self, n_selection, fitnesses):
        return random.choices(self.population, k=n_selection, weights=fitnesses)

    def krzyzowanie(self, bazowy, dodatkowy):
        dziecko = DataSet()

        # Kopiowanie tablicy z rodzica do dziecka1
        dziecko.TablicaKlas = bazowy.TablicaKlas[:]
        dziecko.TablicaSali = bazowy.TablicaSali[:]
        dziecko.TablicaNauczycieli = bazowy.TablicaNauczycieli[:]

        for klasa in range(bazowy.klasy):  # dla kazdej klasy wybieramy losowy termin w tygodniu
            klasa_attempts = 0
            while klasa_attempts < KLASA_MAX_ATTEMPTS:
                losowy_dzien = random.randint(0, DNI_TYGODNIA - 1)
                losowa_lekcja = random.randint(0, bazowy.zajecia - 1)
                nauczyciel, sala = dodatkowy.GetZajecia(KLASA, klasa, losowy_dzien, losowa_lekcja)

                # sprawdzamy czy to nie jest okienko w dodatkowym oraz czy w bazowym zarówno klasa jak i nauczyciel mają wtedy okienko
                if nauczyciel != -1 and dziecko.GetZajecia(KLASA, klasa, losowy_dzien, losowa_lekcja) == OKIENKO and dziecko.GetZajecia(NAUCZYCIEL, nauczyciel, losowy_dzien, losowa_lekcja) == OKIENKO:
                    dzien_w_tygodniu_idx = 0

                    # sprawdzamy czy aktualna klasa ma w swoim tygodniowym planie zajcia z tym nauczycielem za pomocą get tydzien, jesli tak to zapisujemy gdzie
                    for i in dziecko.GetTydzien(KLASA, klasa):
                        if i[0] == nauczyciel:
                            # w tamto miejsce wstawiamy okienko
                            dziecko.Wstaw_okienko(klasa, nauczyciel, i[1], dzien_w_tygodniu_idx // bazowy.zajecia, dzien_w_tygodniu_idx % bazowy.zajecia)
                            dziecko.SetZajecia(klasa, nauczyciel, random.choice(dziecko.Get_free_rooms(losowy_dzien, losowa_lekcja)), losowy_dzien, losowa_lekcja)
                            klasa_attempts = KLASA_MAX_ATTEMPTS  # dokonano zmiany w klasie, nie potrzeba wiecej zmian
                            break
                        dzien_w_tygodniu_idx += 1
                else:
                    klasa_attempts += 1

        return dziecko

    def mutacja(self, osobnik):
        if random.random() < self.prawdopodobienstwo_mutacji:
            liczba_zmian = random.randint(1, 3)
            for _ in range(liczba_zmian):
                osobnik.Random_Swap()
        return osobnik

    def run(self):
        start_time = time.time()
        for generation in range(self.pokolenia):
            new_population = []

            fitnesses = [self.fitness(ind) for ind in self.population]

            # Selekcja
            wybrani = self.selekcja(2*(self.populacja_rozmiar - self.n_elite), fitnesses)

            # Cross-over
            dzieci = []
            for i in range(0, len(wybrani), 2):
                rodzic1 = wybrani[i]
                if i + 1 < len(wybrani):
                    rodzic2 = wybrani[i + 1]
                else:
                    rodzic2 = random.choice(wybrani)
                bazowy, dodatkowy = (rodzic1, rodzic2) if random.random() < 0.5 else (rodzic2, rodzic1)
                dziecko1 = self.krzyzowanie(bazowy, dodatkowy)
                dzieci.append(dziecko1)
                if dziecko1.CheckForRoomCollisions():
                    dziecko1.WypiszPlan()
                    print("dziecko1 po krzyzowaniu ma kolizje sal")

            # Mutacja
            for dziecko in dzieci:
                new_population.append(self.mutacja(dziecko))

            # Elityzm
            elites = sorted(self.population, key=lambda x: self.fitness(x), reverse=True)[:self.n_elite]
            self.population = elites + new_population[:self.populacja_rozmiar - self.n_elite]

            best_individual, best_individual_fitness = self.population_best()
            self.best_fitness_history.append(best_individual_fitness)
            print(f"Generacja {generation + 1}: Najlepszy fitness = {best_individual_fitness}")

            # if best_individual.CheckForRoomCollisions():
            #    best_individual.WypiszPlan()
            #    print("Najlepszy plan ma kolizje sal")

            for fitness_threshold in self.times_to_reach_fitness.keys():
                if best_individual_fitness >= fitness_threshold and self.times_to_reach_fitness[fitness_threshold] is None:
                    self.times_to_reach_fitness[fitness_threshold] = time.time() - start_time
                    self.generations_to_reach_fitness[fitness_threshold] = generation + 1

        best_individual, best_individual_fitness = self.population_best()
        return best_individual, best_individual_fitness, self.best_fitness_history

    def zapisz_czasy(self, filename='fitness_times.txt'):
        with open(filename, 'w') as file:
            for fitness_threshold, czas in self.times_to_reach_fitness.items():
                file.write(
                    f'Fitness {fitness_threshold}: Czas - {czas} sekund, Generacja - {self.generations_to_reach_fitness[fitness_threshold]}\n')

    def rysuj_wykres(self, filename='fitness_wykres.png'):
        plt.plot(self.best_fitness_history)
        plt.xlabel('Pokolenie')
        plt.ylabel('Najlepsza wartość fitness')
        plt.title('Zmiana najlepszej wartości fitness w czasie - SIMPLE')
        plt.savefig(filename)
        plt.show()
