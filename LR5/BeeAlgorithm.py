# Класс для пчелиного алгоритма
import numpy as np
import random
from LR5.Bee import Bee
import tkinter as tk


class BeeAlgorithm:
    def __init__(self, num_scouts, elite_radius, perspective_radius, num_elite, num_perspective, agents_per_perspective,
                 agents_per_elite, bounds, max_epochs, stagnation_limit, fitness_function):
        '''
        - num_scouts (int): Количество пчел-разведчиков в популяции.
        - elite_radius (float): Радиус элитных участков для каждой пчелы.
        - perspective_radius (float): Радиус перспективных участков для каждой пчелы.
        - num_elite (int): Количество элитных участков для обновления координат пчелы.
        - num_perspective (int): Количество перспективных участков для обновления координат пчелы.
        - agents_per_perspective (int): Количество агентов, отправляемых на каждый перспективный участок.
        - agents_per_elite (int): Количество агентов, отправляемых на каждый элитный участок.
        - bounds (list): Границы пространства поиска. Список кортежей, где каждый кортеж - границы для соответствующего измерения.
        - max_epochs (int): Максимальное количество итераций алгоритма.
        - stagnation_limit (int): Количество итераций, после которого процесс считается застойным (условие останова).
        - fitness_function: заданная фитнесс-функция
        '''
        self.num_scouts = num_scouts
        self.elite_radius = elite_radius
        self.perspective_radius = perspective_radius
        self.num_elite = num_elite
        self.num_perspective = num_perspective
        self.agents_per_perspective = agents_per_perspective
        self.agents_per_elite = agents_per_elite
        self.bounds = bounds
        self.max_epochs = max_epochs
        self.stagnation_limit = stagnation_limit
        self.best_bees = []
        self.fitness_function = fitness_function

    def set_options(self, root, ax, canvas, results_text,bound_start,bound_end,target_func):
        self.canvas = canvas
        self.root = root
        self.ax = ax
        self.results_text = results_text
        self.ax = ax
        self.bound_start = bound_start
        self.bound_end = bound_end
        self.target_func = target_func

    def initialize_bees(self):
        bees = []
        for _ in range(self.num_scouts):
            # Инициализация случайных координат для каждой пчелы в пределах заданных границ
            coords = np.array([random.uniform(self.bounds[i][0], self.bounds[i][1]) for i in range(len(self.bounds))], dtype='float')
            bees.append(Bee(coords, self.fitness_function(coords)))
        return bees

    def optimize(self):
        # инициализация начальной популяции пчел
        bees = self.initialize_bees()

        stagnation_count = 0
        best_fitness = float('inf')

        for epoch in range(self.max_epochs):
            # Сортировка пчел по их приспособленности (лучшие впереди)
            bees = sorted(bees, key=lambda bee: bee.fitness)
            self.best_bees = bees[:self.num_elite]

            x_range = np.linspace(self.bound_start, self.bound_end, 100)
            y_range = np.linspace(self.bound_start, self.bound_end, 100)
            X, Y = np.meshgrid(x_range, y_range)
            Z = np.zeros_like(X)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    Z[i, j] = self.target_func(np.array([X[i, j], Y[i, j]]))

            self.ax.cla()
            self.canvas.draw()
            self.ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            self.ax.set_xticks(np.arange(self.bound_start, self.bound_end + 1, 2))
            self.ax.set_yticks(np.arange(self.bound_start, self.bound_end + 1, 2))

            for i in range(self.num_scouts):
                # Исследование окружения для каждой пчелы-разведчика
                self.explore(bees[i])
                # print(bees[i].fitness,bees[i].coords[0],bees[i].coords[1])
                self.ax.scatter(bees[i].coords[0], bees[i].coords[1], bees[i].fitness, color='black',
                           s=10)

            # Выбор лучших пчел из текущей эпохи
            bees = self.select_best(bees)

            # print(bees[i].fitness)
            # Проверка условия стагнации
            current_best_fitness = self.best_bees[0].fitness
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                stagnation_count = 0
            else:
                stagnation_count += 1

            if stagnation_count >= self.stagnation_limit:
                self.results_text.insert(tk.END,f"\nСтагнация. Оптимизация остановлена на итерации {epoch}.\n")
                break


            # self.ax.scatter(self.best_bees[0].coords[0], self.best_bees[0].coords[1], self.best_bees[0].fitness, c="black")
            self.results_text.insert(tk.END,
                                f"Итерация {epoch}: Лучшее решение ({self.best_bees[0].coords[0]:.8f}, {self.best_bees[0].coords[1]:.8f}, {self.best_bees[0].fitness:.8f})\n")
            self.canvas.draw()
            self.results_text.yview_moveto(1)
            self.root.update()
            # print(f'Лучшая пчела в {self.best_bees[0].coords} и фитнесс {self.best_bees[0].fitness}')

        # Последняя сортировка и выбор лучших пчел
        self.best_bees = sorted(bees, key=lambda bee: bee.fitness)[:self.num_elite]
        return self.best_bees[0]

    def explore(self, bee):
        # Случайная фаза исследования соседнего пространства
        phi = random.uniform(-1, 1)
        phi_elite = random.uniform(0, self.elite_radius)
        phi_perspective = random.uniform(0, self.perspective_radius)

        # Выбор случайного направления для каждой координаты
        directions = [random.uniform(-1, 1) for _ in range(len(bee.coords))]

        # Новые координаты для текущей пчелы
        new_coords = [bee.coords[i] + phi * (bee.coords[i] - self.best_bees[0].coords[i]) +
                      phi_elite * (bee.coords[i] - random.choice(self.best_bees).coords[i]) +
                      phi_perspective * random.choice(self.best_bees).coords[i] *
                      directions[i] for i in range(len(bee.coords))]

        # Ограничение координат в пределах заданных границ
        new_coords = np.array(
            [max(min(new_coords[i], self.bounds[i][1]), self.bounds[i][0]) for i in range(len(new_coords))])

        # Вычисление новой приспособленности для пчелы
        new_fitness = self.fitness_function(new_coords)

        # Обновление координат и приспособленности, если новая точка лучше
        if new_fitness < bee.fitness:
            bee.coords = new_coords
            bee.fitness = new_fitness

    def select_best(self, bees):
        # Сортировка всех пчел
        bees.sort(key=lambda bee: bee.fitness)
        # Выбор лучших мест и инициализация новых пчел для заполнения оставшихся мест
        return bees[:self.num_perspective] + self.initialize_bees()[:self.num_scouts - self.num_perspective]

