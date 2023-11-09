import tkinter as tk
from tkinter import ttk
import numpy as np
import time
from tkinter import scrolledtext
from scipy.optimize import minimize


def Simplex_method(frame,root,ax,canvas):
        def target_function(x, y):
            return (2*x ** 2 + 3*y**2 + 4*x*y - 6*x - 3*y)

        def simplex_method(x, y):
            #   global points
            points = []

            def fun(x_i):  # Функция
                x1 = x_i[0]
                x2 = x_i[1]
                return 2 * x1 * x1 + 3 * x2 * x2 + 4 * x1 * x2 - 6 * x1 - 3 * x2

            def callback(x_w):
                g_list = np.ndarray.tolist(x_w)
                g_list.append(fun(x_w))
                points.append(g_list)

            b = (0, float("inf"))  # диапазон поиска
            bounds = (b, b)
            x0 = (x, y)  # начальная точка
            con = {'type': 'eq', 'fun': fun}

            # основной вызов
            res = minimize(fun, x0, method="SLSQP", bounds=bounds,
                           constraints=con, callback=callback)

            glist = np.ndarray.tolist(res.x)
            glist.append(res.fun)
            points.append(glist)

            for iteration, point in enumerate(points):
                yield iteration, point

        def run_optimization():
                res_x = x_var.get()
                res_y = y_var.get()
                delay = delay_var.get()

                x_cs = []
                y_cs = []
                z_cs = []

                # Очистка текущего графика
                ax.cla()

                # Генерация сетки для графика целевой функции
                x_range = np.linspace(x_interval_min.get(), x_interval_max.get(), 100)
                y_range = np.linspace(y_interval_min.get(), y_interval_max.get(), 100)
                X, Y = np.meshgrid(x_range, y_range)
                Z = target_function(X, Y)

                # Построение поверхности графика целевой функции
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xticks(np.arange(x_interval_min.get(), x_interval_max.get() + 1, x_axis_interval.get()))
                ax.set_yticks(np.arange(y_interval_min.get(), y_interval_max.get() + 1, y_axis_interval.get()))
                ax.set_title("Алгоритм Симплекс-метод")

                # Инициализация списка для хранения результатов оптимизации
                results = []

                # Вывод результатов в текстовое поле
                results_text.config(state=tk.NORMAL)
                results_text.delete(1.0, tk.END)

                for i, point in simplex_method(res_x, res_y):
                        x_cs.append(point[0])
                        y_cs.append(point[1])
                        z_cs.append(point[2])

                        # Сохранение результатов и обновление графика
                        results.append((point[0], point[1], i, point[2]))
                        ax.scatter(point[0], point[1], point[2], color='red', s=10)
                        results_text.insert(tk.END,
                                            f"Шаг {i}: Координаты ({point[0]:.2f}, {point[1]:.2f}), Значение функции: {point[2]:.7f}\n")
                        results_text.yview_moveto(1)
                        canvas.draw()
                        root.update()
                        time.sleep(delay)

                # Вывод окончательного результата
                length = len(results) - 1
                ax.scatter(results[length][0], results[length][1], results[length][3], color='black', marker='x', s=60)
                results_text.insert(tk.END,
                                    f"Результат:\nКоординаты ({results[length][0]:.8f}, {results[length][1]:.8f})\nЗначение функции: {results[length][3]:.8f}\n")
                results_text.yview_moveto(1)
                results_text.config(state=tk.DISABLED)


        param_frame2 = frame

        # Параметры задачи
        ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
        ttk.Label(param_frame2, text="Задержка", font=("Helvetica", 10)).grid(row=3, column=0)
        ttk.Label(param_frame2, text="X начальное", font=("Helvetica", 10)).grid(row=1, column=0)
        ttk.Label(param_frame2, text="Y начальное", font=("Helvetica", 10)).grid(row=2, column=0)


        x_var = tk.DoubleVar(value=20)
        y_var = tk.DoubleVar(value=20)
        delay_var = tk.DoubleVar(value=0.5)

        x_entry = ttk.Entry(param_frame2, textvariable=x_var)
        y_entry = ttk.Entry(param_frame2, textvariable=y_var)
        delay_entry = ttk.Entry(param_frame2, textvariable=delay_var)

        x_entry.grid(row=1, column=1)
        y_entry.grid(row=2, column=1)
        delay_entry.grid(row=3, column=1)

        separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
        separator.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

        # Параметры функции
        ttk.Label(param_frame2, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0, pady=10)
        ttk.Label(param_frame2, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
        function_choices = ["2x^2+3y^2+4xy-6x-3y"]
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

