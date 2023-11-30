import tkinter as tk
from tkinter import ttk
import numpy as np
import time
import numdifftools as nd
from tkinter import scrolledtext
from LR4.particleswarm.particle import Particle

def GradientDescentAlgorithm(frame,root,ax,canvas):
    # Функция Химмельблау
    def target_function(x, y):
        return ((x ** 2 + y - 11) ** 2) + ((x + y ** 2 - 7) ** 2)

    # Функция для градиента
    def gradient(function, input):
        ret = np.empty(len(input))
        for i in range(len(input)):
            fg = lambda x: partial_function(function, input, i, x)
            ret[i] = nd.Derivative(fg)(input[i])
        return ret

    # Функция для частной производной
    def partial_function(f___, input, pos, value):
        tmp = input[pos]
        input[pos] = value
        ret = f___(*input)
        input[pos] = tmp
        return ret

    # Функция, которая будет выполнена при нажатии кнопки "Выполнить"
    def run_optimization():
        # Получение параметров оптимизации из пользовательского ввода
        x0 = x_var.get()
        y0 = y_var.get()
        step = step_var.get()
        max_iterations = iterations_var.get()
        delay = delay_var.get()

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
        ax.set_title("Алгоритм градиентного спуска с постоянным шагом")

        # Выбор целевой функции
        function_choice = function_var.get()
        if function_choice == "Функция Химмельблау":
            target_func = target_function

        # Инициализация списка для хранения результатов оптимизации
        results = []

        # Вывод результатов в текстовое поле
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)

        # Основной цикл оптимизации
        for k in range(max_iterations):
            (gx, gy) = gradient(target_func, [x0, y0])

            # Проверка условия остановки
            if np.linalg.norm((gx, gy)) < 0.0001:
                break

            # Обновление координат с учетом шага
            x1, y1 = x0 - step * gx, y0 - step * gy
            f1 = target_func(x1, y1)
            f0 = target_func(x0, y0)

            # Уменьшение шага, если значение функции не уменьшилось
            while not f1 < f0:
                step = step / 2
                x1, y1 = x0 - step * gx, y0 - step * gy
                f1 = target_func(x1, y1)
                f0 = target_func(x0, y0)

            # Проверка на сходимость
            if np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) < 0.0001 and abs(f1 - f0) < 0.0001:
                x0, y0 = x1, y1
                break
            else:
                x0, y0 = x1, y1

            # Сохранение результатов и обновление графика
            results.append((x0, y0, k, f1))
            ax.scatter([x0], [y0], [f1], color='red', s=10)
            results_text.insert(tk.END,
                               f"Шаг {k}: Координаты ({x0:.2f}, {y0:.2f}), Значение функции: {f1:.7f}\n")
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


    # Вкладка для лр1
    param_frame = frame

    # Параметры задачи
    ttk.Label(param_frame, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0,pady=15)
    ttk.Label(param_frame, text="X начальное", font=("Helvetica", 10)).grid(row=1, column=0)
    ttk.Label(param_frame, text="Y начальное", font=("Helvetica", 10)).grid(row=2, column=0)
    ttk.Label(param_frame, text="Шаг", font=("Helvetica", 10)).grid(row=3, column=0)
    ttk.Label(param_frame, text="Число итераций", font=("Helvetica", 10)).grid(row=4, column=0)
    ttk.Label(param_frame, text="Задержка (сек)", font=("Helvetica", 10)).grid(row=5, column=0)

    x_var = tk.DoubleVar(value=-1)
    y_var = tk.DoubleVar(value=-1)
    step_var = tk.DoubleVar(value=0.5)
    iterations_var = tk.IntVar(value=100)
    delay_var = tk.DoubleVar(value=0.5)

    x_entry = ttk.Entry(param_frame, textvariable=x_var)
    y_entry = ttk.Entry(param_frame, textvariable=y_var)
    step_entry = ttk.Entry(param_frame, textvariable=step_var)
    iterations_entry = ttk.Entry(param_frame, textvariable=iterations_var)
    delay_entry = ttk.Entry(param_frame, textvariable=delay_var)

    x_entry.grid(row=1, column=1)
    y_entry.grid(row=2, column=1)
    step_entry.grid(row=3, column=1)
    iterations_entry.grid(row=4, column=1)
    delay_entry.grid(row=5, column=1)

    separator = ttk.Separator(param_frame, orient="horizontal")  # Горизонтальная полоса разделения
    separator.grid(row=7, column=0, columnspan=2, sticky="ew",pady=10)

    # Параметры функции
    ttk.Label(param_frame, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0,pady=10)
    ttk.Label(param_frame, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
    function_choices = ["Функция Химмельблау"]
    function_var = tk.StringVar(value=function_choices[0])
    function_menu = ttk.Combobox(param_frame, textvariable=function_var, values=function_choices,width=22)
    function_menu.grid(row=10, column=1,pady=5)
    ttk.Label(param_frame, text="X интервал (min)", font=("Helvetica", 10)).grid(row=11, column=0)
    ttk.Label(param_frame, text="X интервал (max)", font=("Helvetica", 10)).grid(row=12, column=0)
    ttk.Label(param_frame, text="Y интервал (min)", font=("Helvetica", 10)).grid(row=13, column=0)
    ttk.Label(param_frame, text="Y интервал (max)", font=("Helvetica", 10)).grid(row=14, column=0)
    ttk.Label(param_frame, text="Ось X интервал", font=("Helvetica", 10)).grid(row=16, column=0)
    ttk.Label(param_frame, text="Ось Y интервал", font=("Helvetica", 10)).grid(row=17, column=0)

    separator = ttk.Separator(param_frame, orient="horizontal")  # Горизонтальная полоса разделения
    separator.grid(row=18, column=0,columnspan=2, sticky="ew",pady=10)

    x_interval_min = tk.DoubleVar(value=-5)
    x_interval_max = tk.DoubleVar(value=5)
    y_interval_min = tk.DoubleVar(value=-5)
    y_interval_max = tk.DoubleVar(value=5)
    x_axis_interval = tk.IntVar(value=2)
    y_axis_interval = tk.IntVar(value=2)

    x_interval_min_entry = ttk.Entry(param_frame, textvariable=x_interval_min)
    x_interval_max_entry = ttk.Entry(param_frame, textvariable=x_interval_max)
    y_interval_min_entry = ttk.Entry(param_frame, textvariable=y_interval_min)
    y_interval_max_entry = ttk.Entry(param_frame, textvariable=y_interval_max)
    x_axis_interval_entry = ttk.Entry(param_frame, textvariable=x_axis_interval)
    y_axis_interval_entry = ttk.Entry(param_frame, textvariable=y_axis_interval)

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
    apply_settings_button = ttk.Button(param_frame, text="Выполнить", command=run_optimization, style="My.TButton")
    apply_settings_button.grid(row=21, column=1, padx=10, pady=10)

    ttk.Label(param_frame, text="Выполнение и результаты", font=("Helvetica", 12)).grid(row=20, column=0,pady=10)
    results_text = scrolledtext.ScrolledText(param_frame, wrap=tk.WORD, height=18, width=40,padx=2, state=tk.DISABLED)
    results_text.grid(row=21, column=0,padx=10)
