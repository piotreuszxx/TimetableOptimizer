import time
from Consts import *
from GeneticAlgorithm import GeneticAlgorithm

if __name__ == "__main__":
    start_time = time.time()

    algorithm = GeneticAlgorithm(populacja_rozmiar=100, pokolenia=2000, prawdopodobienstwo_mutacji=0.6, n_elite=10, rodzaj_oceny=BETTER)
    najlepszy_osobnik, najlepszy_fitness, fitness_w_pokoleniach = algorithm.run()

    print("Najlepszy plan zajęć:")
    najlepszy_osobnik.WypiszPlan()
    print(f"Ocena fitness najlepszego planu: {najlepszy_fitness}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Czas działania programu: {elapsed_time} sekund")

    if najlepszy_osobnik.CheckForRoomCollisions():
        print("Najlepszy plan ma kolizje sal")
    else:
        print("Najlepszy plan nie ma kolizji sal")

    najlepszy_osobnik.CountOkienka()
    algorithm.rysuj_wykres('fitness_wykres.png')
    algorithm.zapisz_czasy('fitness_times.txt')
