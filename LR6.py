import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np
import math
import random
from operator import itemgetter
import time


def ImmuneAlgorithm(frame,root,ax,canvas):

        # Функция Розенброка для оптимизации
        def rosenbrock_function(x,y):
            return (1.0 - x) ** 2 + 100.0 * (y - x * x) ** 2

        class AIS:
            def __init__(self, iter_number, num_antibodies, num_best, num_random, num_clones, mutation_rate,
                         x_range,
                         y_range):
                self.iter_number = iter_number
                self.num_antibodies = num_antibodies
                self.num_best = num_best
                self.num_random = num_random
                self.num_clones = num_clones
                self.mutation_rate = mutation_rate
                self.x_range = x_range
                self.y_range = y_range

                self.antibodies = [[random.uniform(self.x_range[0], self.x_range[1]),
                                    random.uniform(self.y_range[0], self.y_range[1]),
                                    0.0] for _ in range(self.num_antibodies)]
                for antibody in self.antibodies:
                    antibody[2] =  rosenbrock_function(antibody[0], antibody[1])


                self.antibody_best = min(self.antibodies, key=itemgetter(2))

            def sort_antibodies(self):
                self.antibodies.sort(key=lambda x: x[2])

            def mutate(self, antibody):
                new_x_val = np.clip(antibody[0] + self.mutation_rate * np.random.randn(), self.x_range[0],
                                    self.x_range[1])
                new_y_val = np.clip(antibody[1] + self.mutation_rate * np.random.randn(), self.y_range[0],
                                    self.y_range[1])
                return [new_x_val, new_y_val, rosenbrock_function(new_x_val, new_y_val)]

            def next_iteration(self):
                for iteration in range(self.iter_number):
                    self.sort_antibodies()

                    for i in range(self.num_best, self.num_antibodies):
                        if i < self.num_best + self.num_random:
                            self.antibodies[i] = [random.uniform(self.x_range[0], self.x_range[1]),
                                                  random.uniform(self.y_range[0], self.y_range[1]),
                                                  0.0]
                            self.antibodies[i][2] = rosenbrock_function(self.antibodies[i][0], self.antibodies[i][1])
                        else:
                            self.antibodies[i] = self.mutate(self.antibodies[i - self.num_random])
                            self.antibodies[i][2] = rosenbrock_function(self.antibodies[i][0], self.antibodies[i][1])

                    self.antibody_best = min(self.antibodies, key=itemgetter(2))

        def run_optimization():

            iter_number = iterations_var.get()
            antibodies_num = antibodies_number_var.get()
            best_num = best_number_var.get()
            random_num = random_number_var.get()
            clones_num = clones_number_var.get()
            mutation_coef = mutation_rate_var.get()
            delay = delay_var.get()

            # Генерация сетки для графика целевой функции
            x_range = np.linspace(x_interval_min.get(), x_interval_max.get(), 100)
            y_range = np.linspace(y_interval_min.get(), y_interval_max.get(), 100)
            X, Y = np.meshgrid(x_range, y_range)
            Z = rosenbrock_function(X, Y)

            ax.cla()
            # Построение поверхности графика целевой функции
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_xticks(np.arange(x_interval_min.get(), x_interval_max.get() + 1, x_axis_interval.get()))
            ax.set_yticks(np.arange(y_interval_min.get(), y_interval_max.get() + 1, y_axis_interval.get()))
            ax.set_title("Иммунный алгоритм")

            ais = AIS(iter_number, antibodies_num, best_num, random_num, clones_num, mutation_coef,
                      [x_interval_min.get(), x_interval_max.get()], [y_interval_min.get(), y_interval_max.get()])

            # отрисовка стартовой популяции
            for antibody in ais.antibodies:
                ax.scatter(antibody[0], antibody[1], antibody[2], c="red", s=10)

            # ax.scatter(ais.antibody_best[0], ais.antibody_best[1], ais.antibody_best[2], c="blue")
            canvas.draw()
            root.update()

            # очистка графика
            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
            canvas.draw()

            cnt = 0
            results_text.config(state=tk.NORMAL)
            results_text.delete(1.0, tk.END)
            # отрисовка промежуточной популяции и эволюция
            for i in range(iter_number):
                prev_antibody_best = ais.antibody_best
                ais.next_iteration()

                # подсчет продолжительности стагнации
                if abs(prev_antibody_best[2] - ais.antibody_best[2]) < 0.0001:
                    cnt += 1
                else:
                    cnt = 0

                if cnt == 15:
                    break

                # отрисовка промежуточной популяции
                for antibody in ais.antibodies:
                    ax.scatter(antibody[0], antibody[1], antibody[2], c="red", s=10)

                # ax.scatter(ais.antibody_best[0], ais.antibody_best[1], ais.antibody_best[2], c="blue")
                results_text.insert(tk.END,
                                    f"Шаг {i}: Координаты ({ais.antibody_best[0]:.4f}, "
                                    f"{ais.antibody_best[1]:.4f}),"
                                    f" Значение функции: {ais.antibody_best[2]:.4f}\n")
                results_text.yview_moveto(1)

                canvas.draw()
                root.update()
                time.sleep(delay)

                # очистка графика
                ax.cla()
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
                canvas.draw()

            # отрисовка результирующей популяции
            for antibody in ais.antibodies:
                ax.scatter(antibody[0], antibody[1], antibody[2], c="red", s=10)

            ax.scatter(ais.antibody_best[0], ais.antibody_best[1], ais.antibody_best[2], c='black', marker='x', s=60)

            canvas.draw()
            root.update()
            results_text.insert(tk.END,
                                f"Результат:\nКоординаты ({ais.antibody_best[0]:.5f}, "
                                f"{ais.antibody_best[1]:.5f}),\nЗначение функции: {ais.antibody_best[2]:.8f}\n")
            results_text.yview_moveto(1)
            results_text.config(state=tk.DISABLED)

        param_frame2 = frame

        # Параметры задачи
        ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
        ttk.Label(param_frame2, text="Итераций", font=("Helvetica", 10)).grid(row=1, column=0)
        ttk.Label(param_frame2, text="Количество антител", font=("Helvetica", 10)).grid(row=2, column=0)
        ttk.Label(param_frame2, text="Количество лучших антител", font=("Helvetica", 10)).grid(row=3, column=0)
        ttk.Label(param_frame2, text="Количество случайных антител", font=("Helvetica", 10)).grid(row=4, column=0)
        ttk.Label(param_frame2, text="Количество клонов", font=("Helvetica", 10)).grid(row=5, column=0)
        ttk.Label(param_frame2, text="Коэффициент мутаций", font=("Helvetica", 10)).grid(row=6, column=0)
        ttk.Label(param_frame2, text="Задержка", font=("Helvetica", 10)).grid(row=7, column=0)

        iterations_var = tk.IntVar(value=200)
        antibodies_number_var = tk.IntVar(value=50)
        best_number_var = tk.IntVar(value=10)
        random_number_var = tk.IntVar(value=10)
        clones_number_var = tk.IntVar(value=20)
        mutation_rate_var = tk.DoubleVar(value=0.2)
        delay_var = tk.DoubleVar(value=0.01)

        iterations_entry = ttk.Entry(param_frame2, textvariable=iterations_var)
        antibodies_number_entry = ttk.Entry(param_frame2, textvariable=antibodies_number_var)
        best_number_entry = ttk.Entry(param_frame2, textvariable=best_number_var)
        random_number_entry = ttk.Entry(param_frame2, textvariable=random_number_var)
        clones_number_entry = ttk.Entry(param_frame2, textvariable=clones_number_var)
        mutation_rate_entry = ttk.Entry(param_frame2, textvariable=mutation_rate_var)
        delay_entry = ttk.Entry(param_frame2, textvariable=delay_var)

        iterations_entry.grid(row=1, column=1)
        antibodies_number_entry.grid(row=2, column=1)
        best_number_entry.grid(row=3, column=1)
        random_number_entry.grid(row=4, column=1)
        clones_number_entry.grid(row=5, column=1)
        mutation_rate_entry.grid(row=6, column=1)
        delay_entry.grid(row=7, column=1)

        separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
        separator.grid(row=8, column=0, columnspan=2, sticky="ew", pady=10)

        # Параметры функции

        ttk.Label(param_frame2, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0, pady=10)
        ttk.Label(param_frame2, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
        function_choices = ["Функция Розенброка"]
        function_var = tk.StringVar(value=function_choices[0])
        function_menu = ttk.Combobox(param_frame2, textvariable=function_var, values=function_choices, width=22)
        function_menu.grid(row=10, column=1, pady=5)
        ttk.Label(param_frame2, text="X интервал (min)", font=("Helvetica", 10)).grid(row=11, column=0)
        ttk.Label(param_frame2, text="X интервал (max)", font=("Helvetica", 10)).grid(row=12, column=0)
        ttk.Label(param_frame2, text="Y интервал (min)", font=("Helvetica", 10)).grid(row=13, column=0)
        ttk.Label(param_frame2, text="Y интервал (max)", font=("Helvetica", 10)).grid(row=14, column=0)
        ttk.Label(param_frame2, text="Ось X интервал", font=("Helvetica", 10)).grid(row=16, column=0)
        ttk.Label(param_frame2, text="Ось Y интервал", font=("Helvetica", 10)).grid(row=17, column=0)

        separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
        separator.grid(row=18, column=0, columnspan=2, sticky="ew", pady=10)

        x_interval_min = tk.DoubleVar(value=-5)
        x_interval_max = tk.DoubleVar(value=5)
        y_interval_min = tk.DoubleVar(value=-5)
        y_interval_max = tk.DoubleVar(value=5)
        x_axis_interval = tk.IntVar(value=2)
        y_axis_interval = tk.IntVar(value=2)

        x_interval_min_entry = ttk.Entry(param_frame2, textvariable=x_interval_min)
        x_interval_max_entry = ttk.Entry(param_frame2, textvariable=x_interval_max)
        y_interval_min_entry = ttk.Entry(param_frame2, textvariable=y_interval_min)
        y_interval_max_entry = ttk.Entry(param_frame2, textvariable=y_interval_max)
        x_axis_interval_entry = ttk.Entry(param_frame2, textvariable=x_axis_interval)
        y_axis_interval_entry = ttk.Entry(param_frame2, textvariable=y_axis_interval)

        x_interval_min_entry.grid(row=11, column=1)
        x_interval_max_entry.grid(row=12, column=1)
        y_interval_min_entry.grid(row=13, column=1)
        y_interval_max_entry.grid(row=14, column=1)
        x_axis_interval_entry.grid(row=16, column=1)
        y_axis_interval_entry.grid(row=17, column=1)

        # Создание кнопки Выполнить
        button_style = ttk.Style()
        button_style.configure("My.TButton", font=("Helvetica", 14))

        # Создание кнопки Выполнить
        apply_settings_button = ttk.Button(param_frame2, text="Выполнить",command=run_optimization, style="My.TButton")
        apply_settings_button.grid(row=21, column=1, padx=10, pady=10)

        ttk.Label(param_frame2, text="Выполнение и результаты", font=("Helvetica", 12)).grid(row=18, column=0, pady=10)
        results_text = scrolledtext.ScrolledText(param_frame2, wrap=tk.WORD, height=16, width=40, padx=2, state=tk.DISABLED)
        results_text.grid(row=21, column=0, padx=10)
        root.mainloop()

