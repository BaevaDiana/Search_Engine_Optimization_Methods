import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import numdifftools as nd
from tkinter import scrolledtext
from LR1 import GradientDescentAlgorithm


def target_function(x, y):
    return (2*x ** 2 + 3*y**2 + 4*x*y - 6*x - 3*y)

def run_optimization():
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
        if function_choice == "Функция для симпликс-метода":
            target_func = target_function

        # Инициализация списка для хранения результатов оптимизации
        results = []

        # Вывод результатов в текстовое поле
        results_text.config(state=tk.NORMAL)
        results_text.delete(1.0, tk.END)


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


# Создание окна приложения
root = tk.Tk()
root.title("Методы поисковой оптимизации")

notebook = ttk.Notebook(root)
notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


# Вкладка для лр1
param_frame = ttk.Frame(notebook,padding=(15, 0))
notebook.add(param_frame, text="ЛР1")

GradientDescentAlgorithm(param_frame,root)

param_frame2 = ttk.Frame(notebook)
notebook.add(param_frame2, text="ЛР2")

param_frame3 = ttk.Frame(notebook)
notebook.add(param_frame3, text="ЛР3")

param_frame4 = ttk.Frame(notebook)
notebook.add(param_frame4, text="ЛР4")

param_frame5 = ttk.Frame(notebook)
notebook.add(param_frame5, text="ЛР5")

param_frame6 = ttk.Frame(notebook)
notebook.add(param_frame6, text="ЛР6")

param_frame7 = ttk.Frame(notebook)
notebook.add(param_frame7, text="ЛР7")

param_frame8 = ttk.Frame(notebook)
notebook.add(param_frame8, text="ЛР8")

# Параметры задачи
ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
ttk.Label(param_frame2, text="Задержка", font=("Helvetica", 10)).grid(row=1, column=0)

delay_var = tk.DoubleVar(value=0.5)
delay_entry = ttk.Entry(param_frame, textvariable=delay_var)
delay_entry.grid(row=5, column=1)



separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
separator.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

# Параметры функции
ttk.Label(param_frame2, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0, pady=10)
ttk.Label(param_frame2, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
function_choices = ["Функция Химмельблау"]
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
apply_settings_button = ttk.Button(param_frame2, text="Выполнить", style="My.TButton")
apply_settings_button.grid(row=21, column=1, padx=10, pady=10)

ttk.Label(param_frame2, text="Выполнение и результаты", font=("Helvetica", 12)).grid(row=20, column=0, pady=10)
results_text = scrolledtext.ScrolledText(param_frame2, wrap=tk.WORD, height=18, width=40, padx=2, state=tk.DISABLED)
results_text.grid(row=21, column=0, padx=10)

# Инициализация графика при запуске программы
fig = plt.figure(figsize=(8, 9))  # Установка размеров фигуры (ширина, высота)
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Алгоритм градиентного спуска с постоянным шагом")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, padx=20)

root.mainloop()
