import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np
import math
from LR5.BeeAlgorithm import BeeAlgorithm


def BeesAlgorithm(frame,root,ax,canvas):

        # Функция Розенброка для оптимизации
        def himel_function(x_arr):
            x, y = x_arr[0], x_arr[1]
            return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2

        def rosenbrock_function(x_arr):
            x, y = x_arr[0], x_arr[1]
            return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

        def rastrigin(x_arr):
            size = len(x_arr)
            return 10 * size + np.sum(x_arr ** 2 - 10 * np.cos(2 * np.pi * x_arr))

        def run_optimization():
            ax.cla()
            function_choice = function_var.get()
            target_func = himel_function
            if function_choice == "Функция Химмельблау":
                target_func = himel_function
            elif function_choice == "Функция Розенброка":
                target_func = rosenbrock_function
            elif function_choice == "Функция Растригина":
                target_func = rastrigin



            iterations=int(iteration.get())
            scout = int(scouts.get())  # разведчики
            perspective_B = int(perspective_b.get())
            best_B = int(best_b.get())  # лучшие пчелы
            perspective_A = int(perspective_a.get())
            best_A  = int(best_a.get())
            size_A = int(size_a.get())
            Delay = int(delay.get())

            bound_start = float(x_interval_min.get())
            bound_end = float(x_interval_max.get())
            bounds = [(bound_start, bound_end) for i in range(2)]


            x_range = np.linspace(bound_start, bound_end, 100)
            y_range = np.linspace(bound_start, bound_end, 100)
            X, Y = np.meshgrid(x_range, y_range)
            Z = np.zeros_like(X)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    Z[i, j] = target_func(np.array([X[i, j], Y[i, j]]))

            ax.cla()
            canvas.draw()
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_xticks(np.arange(bound_start, bound_end + 1, 2))
            ax.set_yticks(np.arange(bound_start, bound_end + 1, 2))


            results_text.config(state=tk.NORMAL)
            results_text.delete(1.0, tk.END)
            algorithm = BeeAlgorithm(scout, size_A, size_A, best_A, perspective_A,
                                     perspective_B, best_B, bounds, iterations, 20,
                                     target_func)
            algorithm.set_options(root, ax, canvas, results_text)
            best_bee = algorithm.optimize()
            ax.scatter(best_bee.coords[0], best_bee.coords[1], best_bee.fitness, c="red")
            results_text.insert(tk.END,
                                f"Лучшее решение ({best_bee.coords[0]:.8f}, {best_bee.coords[1]:.8f}, {best_bee.fitness:.8f})\n")

            canvas.draw()
            root.update()


        param_frame2 = frame

        # Параметры задачи
        ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
        ttk.Label(param_frame2, text="Итераций", font=("Helvetica", 10)).grid(row=1, column=0)
        ttk.Label(param_frame2, text="Разведчики", font=("Helvetica", 10)).grid(row=2, column=0)
        ttk.Label(param_frame2, text="Пчел в перспективном участке", font=("Helvetica", 10)).grid(row=3, column=0)
        ttk.Label(param_frame2, text="Пчел в улчшем участке", font=("Helvetica", 10)).grid(row=4, column=0)
        ttk.Label(param_frame2, text="Перспективных участков", font=("Helvetica", 10)).grid(row=5, column=0)
        ttk.Label(param_frame2, text="Лучших участков", font=("Helvetica", 10)).grid(row=6, column=0)
        ttk.Label(param_frame2, text="Размер участков", font=("Helvetica", 10)).grid(row=7, column=0)
        ttk.Label(param_frame2, text="Задержка", font=("Helvetica", 10)).grid(row=8, column=0)


        iteration = tk.IntVar(value=200)
        scouts = tk.IntVar(value=20) #разведчики
        perspective_b = tk.IntVar(value=10) #перспективных пчел
        best_b = tk.IntVar(value=20) #лучшие пчелы
        perspective_a  = tk.IntVar(value=3) #перпективных участков
        best_a = tk.IntVar(value=1)  # лучших участков
        size_a = tk.DoubleVar(value=0.5)  # размер участков
        delay = tk.DoubleVar(value=0.03)  # задержка

        iteration_entry = ttk.Entry(param_frame2, textvariable=iteration)
        scouts_entry = ttk.Entry(param_frame2, textvariable=scouts)
        perspective_b_entry = ttk.Entry(param_frame2, textvariable=perspective_b)
        best_b_entry = ttk.Entry(param_frame2, textvariable=best_b)
        perspective_a_entry = ttk.Entry(param_frame2, textvariable=perspective_a)
        best_a_entry = ttk.Entry(param_frame2, textvariable=best_a)
        size_a_entry = ttk.Entry(param_frame2, textvariable=size_a)
        delay_entry = ttk.Entry(param_frame2, textvariable=delay)

        iteration_entry.grid(row=1, column=1)
        scouts_entry.grid(row=2, column=1)
        perspective_b_entry.grid(row=3, column=1)
        best_b_entry.grid(row=4, column=1)
        perspective_a_entry.grid(row=5, column=1)
        best_a_entry.grid(row=6, column=1)
        size_a_entry.grid(row=7, column=1)
        delay_entry.grid(row=8, column=1)


        separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
        separator.grid(row=9, column=0, columnspan=2, sticky="ew", pady=10)

        # Параметры функции
        ttk.Label(param_frame2, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0, pady=10)
        ttk.Label(param_frame2, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
        function_choices = ["Нажмите для выбора","Функция Химмельблау", "Функция Розенброка",
                        "Функция Растригина"]
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

        ttk.Label(param_frame2, text="Выполнение и результаты", font=("Helvetica", 12)).grid(row=20, column=0, pady=10)
        results_text = scrolledtext.ScrolledText(param_frame2, wrap=tk.WORD, height=18, width=40, padx=2, state=tk.DISABLED)
        results_text.grid(row=21, column=0, padx=10)
        root.mainloop()

