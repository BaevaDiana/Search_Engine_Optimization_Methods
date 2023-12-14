import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np
import random
from operator import itemgetter
import time


def BFO(frame,root,ax,canvas):
        # Функция Розенброка для оптимизации
        def sphere(x, y):
                return x ** 2 + y ** 2

        class BFO:
                def __init__(self, num_bacteries, chemotaxis_steps, num_to_eliminate,
                             elimination_probability, x_range, y_range):
                        self.num_bacteries = num_bacteries
                        self.chemotaxis_steps = chemotaxis_steps
                        self.num_to_eliminate = num_to_eliminate
                        self.elimination_probability = elimination_probability
                        self.x_range = x_range
                        self.y_range = y_range

                        self.bacteries = [[random.uniform(self.x_range[0], self.x_range[1]),
                                           random.uniform(self.y_range[0], self.y_range[1]),
                                           0.0] for _ in range(self.num_bacteries)]
                        for bacteria in self.bacteries:
                                bacteria[2] = sphere(bacteria[0], bacteria[1])

                        self.bacteria_best = min(self.bacteries, key=itemgetter(2))
                        self.hp = [bacteria[2] for bacteria in self.bacteries]

                def next_iteration(self):
                        for i in range(self.num_bacteries):
                                # хемотаксис
                                for t in range(self.chemotaxis_steps):
                                        step = np.random.uniform(-1, 1)
                                        new_x = np.clip(self.bacteries[i][0] + step, self.x_range[0], self.x_range[1])
                                        new_y = np.clip(self.bacteries[i][1] + step, self.y_range[0], self.y_range[1])

                                        new_fitness = sphere(new_x, new_y)

                                        if new_fitness < self.bacteries[i][2]:
                                                self.bacteries[i][0] = new_x
                                                self.bacteries[i][1] = new_y
                                                self.bacteries[i][2] = new_fitness
                                                # break

                                # репродукция
                                self.hp[i] += self.bacteries[i][2]

                        # Сортировка бактерий в порядке возрастания состояний здоровья
                        sorted_indices = np.argsort(self.hp)
                        self.bacteries = [self.bacteries[i] for i in sorted_indices]
                        self.hp = [self.hp[i] for i in sorted_indices]

                        # Замена второй половины бактерий первой
                        half_point = self.num_bacteries // 2
                        self.bacteries[:half_point], self.bacteries[half_point:] = self.bacteries[
                                                                                   half_point:], self.bacteries[
                                                                                                 :half_point]
                        self.hp[:half_point], self.hp[half_point:] = self.hp[half_point:], self.hp[:half_point]

                        # Ликвидация и рассеивание
                        indices_to_eliminate = np.random.choice(self.num_bacteries, size=self.num_to_eliminate,
                                                                replace=False)
                        for i in indices_to_eliminate:
                                if np.random.rand() > self.elimination_probability:
                                        self.bacteries[i] = [random.uniform(self.x_range[0], self.x_range[1]),
                                                             random.uniform(self.y_range[0], self.y_range[1]),
                                                             0]
                                        self.bacteries[i][2] = sphere(self.bacteries[i][0], self.bacteries[i][1])

                        self.bacteria_best = min(self.bacteries, key=itemgetter(2))

        def run_optimization():

                iter_number = iterations_var.get()
                bacteries_number = bacteries_number_var.get()
                steps_of_chemotaxis = chemotaxis_steps_var.get()
                eliminate_number = num_to_eliminate_var.get()
                elimination_prob = elimination_probability_var.get()
                delay = delay_var.get()

                # Генерация сетки для графика целевой функции
                x_range = np.linspace(x_interval_min.get(), x_interval_max.get(), 100)
                y_range = np.linspace(y_interval_min.get(), y_interval_max.get(), 100)
                X, Y = np.meshgrid(x_range, y_range)
                Z = sphere(X, Y)

                ax.cla()
                # Построение поверхности графика целевой функции
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xticks(np.arange(x_interval_min.get(), x_interval_max.get() + 1, x_axis_interval.get()))
                ax.set_yticks(np.arange(y_interval_min.get(), y_interval_max.get() + 1, y_axis_interval.get()))
                ax.set_title("Иммунный алгоритм")

                bfo = BFO(bacteries_number, steps_of_chemotaxis, eliminate_number, elimination_prob,
                          [x_interval_min.get(), x_interval_max.get()], [y_interval_min.get(), y_interval_max.get()])

                # отрисовка стартовой популяции
                for bacteria in bfo.bacteries:
                        ax.scatter(bacteria[0], bacteria[1], bacteria[2], c="red", s=10)

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
                        bfo.next_iteration()
                        for bacteria in bfo.bacteries:
                                # отрисовка промежуточной популяции
                                ax.scatter(bacteria[0], bacteria[1], bacteria[2], c="red", s=10)

                        # ax.scatter(bfo.bacteria_best[0], bfo.bacteria_best[1], bfo.bacteria_best[2], c="blue")
                        results_text.insert(tk.END,
                                            f"Шаг {i}: Координаты ({bfo.bacteria_best[0]:.4f}, "
                                            f"{bfo.bacteria_best[1]:.4f}),"
                                            f" Значение функции: {bfo.bacteria_best[2]:.4f}\n")
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
                for bacteria in bfo.bacteries:
                        ax.scatter(bacteria[0], bacteria[1], bacteria[2], c="red", s=10)

                ax.scatter(bfo.bacteria_best[0], bfo.bacteria_best[1], bfo.bacteria_best[2], c='black', marker='x',
                           s=60)

                canvas.draw()
                root.update()
                results_text.insert(tk.END,
                                    f"Результат:\nКоординаты ({bfo.bacteria_best[0]:.5f}, "
                                    f"{bfo.bacteria_best[1]:.5f}),\nЗначение функции: {bfo.bacteria_best[2]:.8f}\n")
                results_text.yview_moveto(1)
                results_text.config(state=tk.DISABLED)


        param_frame2 = frame

        # Параметры задачи
        ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
        ttk.Label(param_frame2, text="Количество итераций", font=("Helvetica", 10)).grid(row=1, column=0)
        ttk.Label(param_frame2, text="Количество бактерий", font=("Helvetica", 10)).grid(row=2, column=0)
        ttk.Label(param_frame2, text="Шагов хемотаксиса", font=("Helvetica", 10)).grid(row=3, column=0)
        ttk.Label(param_frame2, text="Количество ликвидируемых", font=("Helvetica", 10)).grid(row=4, column=0)
        ttk.Label(param_frame2, text="Вероятность ликвидации", font=("Helvetica", 10)).grid(row=5, column=0)
        ttk.Label(param_frame2, text="Задержка", font=("Helvetica", 10)).grid(row=6, column=0)

        iterations_var = tk.IntVar(value=50)
        bacteries_number_var = tk.IntVar(value=50)
        chemotaxis_steps_var = tk.IntVar(value=15)
        num_to_eliminate_var = tk.IntVar(value=20)
        elimination_probability_var = tk.DoubleVar(value=0.6)
        delay_var = tk.DoubleVar(value=0.01)

        iterations_entry = ttk.Entry(param_frame2, textvariable=iterations_var)
        bacteries_number_entry = ttk.Entry(param_frame2, textvariable=bacteries_number_var)
        chemotaxis_steps_entry = ttk.Entry(param_frame2, textvariable=chemotaxis_steps_var)
        num_to_eliminate_entry = ttk.Entry(param_frame2, textvariable=num_to_eliminate_var)
        elimination_probability_entry = ttk.Entry(param_frame2, textvariable=elimination_probability_var)
        delay_entry = ttk.Entry(param_frame2, textvariable=delay_var)

        iterations_entry.grid(row=1, column=1)
        bacteries_number_entry.grid(row=2, column=1)
        chemotaxis_steps_entry.grid(row=3, column=1)
        num_to_eliminate_entry.grid(row=4, column=1)
        elimination_probability_entry.grid(row=5, column=1)
        delay_entry.grid(row=6, column=1)


        separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
        separator.grid(row=9, column=0, columnspan=2, sticky="ew", pady=10)

        # Параметры функции
        ttk.Label(param_frame2, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0, pady=10)
        ttk.Label(param_frame2, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
        function_choices = ["Функция сферы"]
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

