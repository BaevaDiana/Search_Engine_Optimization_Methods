import tkinter as tk
from tkinter import ttk
import numpy as np
import time
from tkinter import scrolledtext

from matplotlib.colors import LinearSegmentedColormap
from random import uniform, random


class GeneticAlgorithm:
    def __init__(self, func, generations, pop_number, x_range, y_range, mut_chance=0.8, survive_cof=0.8):
        self.func = func
        self.population = dict()
        self.mut_chance = mut_chance
        self.survive_cof = survive_cof
        self.generations = generations
        self.pop_number = pop_number
        self.x_range = x_range
        self.y_range = y_range

    def generate_start_population(self):
        for i in range(self.pop_number):
            po_x = np.clip(uniform(self.x_range[0], self.x_range[1]), self.x_range[0], self.x_range[1])
            po_y = np.clip(uniform(self.y_range[0], self.y_range[1]), self.y_range[0], self.y_range[1])
            self.population[i] = [po_x, po_y, self.func(po_x, po_y)]

    def get_best_individual(self):
        return min(self.population.items(), key=lambda item: item[1][2])

    def select(self):
        sorted_pop = dict(sorted(self.population.items(), key=lambda item: item[1][2], reverse=True))

        cof = int(self.pop_number * (1 - self.survive_cof))
        parents1 = list(sorted_pop.items())[cof: cof * 2]
        parents2 = list(sorted_pop.items())[self.pop_number - cof: self.pop_number]

        i = 0
        for pop in sorted_pop.values():
            if random() > 0.5:
                pop[0] = parents1[i][1][0]
                pop[1] = parents2[i][1][1]
                pop[2] = self.func(parents1[i][1][0], parents2[i][1][1])
            else:
                pop[0] = parents2[i][1][0]
                pop[1] = parents1[i][1][1]
                pop[2] = self.func(parents2[i][1][0], parents1[i][1][1])
            i += 1
            if i >= cof:
                break

        self.population = sorted_pop

    def mutation(self, cur_gen):
        for pop in self.population.values():
            if random() < self.mut_chance:
                pop[0] += (random() - 0.5) * ((self.generations - cur_gen) / self.generations)
            if random() < self.mut_chance:
                pop[1] += (random() - 0.5) * ((self.generations - cur_gen) / self.generations)
            pop[2] = self.func(pop[0], pop[1])