import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import numdifftools as nd

# Определение функций, которые мы можем оптимизировать
def target_function(x, y):
    result = ((x ** 2 + y - 11) ** 2) + ((x + y ** 2 - 7) ** 2)
    return np.round(result, 6)

# Определение функции для обновления графика функции
def update_function_plot():
    ax.cla()
    x_range = np.linspace(x_interval_min.get(), x_interval_max.get(), 100)
    y_range = np.linspace(y_interval_min.get(), y_interval_max.get(), 100)
    X, Y = np.meshgrid(x_range, y_range)
    Z = target_function(X, Y)
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xticks(np.arange(x_interval_min.get(), x_interval_max.get() + 1, x_axis_interval.get()))
    ax.set_yticks(np.arange(y_interval_min.get(), y_interval_max.get() + 1, y_axis_interval.get()))
    canvas.draw()
    run_optimization()

# Функция для обновления поля "Выполнение и результаты"
def update_results(text_widget, results):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    for result in results:
        text_widget.insert(tk.END,
                           f"Шаг {result[2]}: Координаты ({result[0]:.2f}, {result[1]:.2f}), Значение функции: {result[3]:.4f}\n")
    text_widget.config(state=tk.DISABLED)

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
    x0 = x_var.get()
    y0 = y_var.get()
    step = step_var.get()
    max_iterations = iterations_var.get()
    delay = delay_var.get()

    ax.cla()
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    function_choice = function_var.get()
    if function_choice == "Функция Химмельблау":
        target_func = target_function

    results = []

    for k in range(max_iterations):
        (gx, gy) = gradient(target_func, [x0, y0])

        if np.linalg.norm((gx, gy)) < 0.0001:
            break

        x1, y1 = x0 - step * gx, y0 - step * gy
        f1 = target_func(x1, y1)
        f0 = target_func(x0, y0)

        while not f1 < f0:
            step = step / 2
            x1, y1 = x0 - step * gx, y0 - step * gy
            f1 = target_func(x1, y1)
            f0 = target_func(x0, y0)

        if np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) < 0.0001 and abs(f1 - f0) < 0.0001:
            x0, y0 = x1, y1
            break
        else:
            x0, y0 = x1, y1

        results.append((x0, y0, k, round(f1,5)))
        ax.scatter([x0], [y0], [round(f1,5)], color='red')

        canvas.draw()
        root.update()
        time.sleep(delay)

    update_results(results_text, results)

# Создание окна приложения
root = tk.Tk()
root.title("Градиентный спуск")

# Создание интерфейса для параметров оптимизации
param_frame = ttk.Frame(root)
param_frame.pack(side=tk.LEFT, padx=10, pady=10)

ttk.Label(param_frame, text="X начальное").grid(row=1, column=0)
ttk.Label(param_frame, text="Y начальное").grid(row=2, column=0)
ttk.Label(param_frame, text="Шаг").grid(row=3, column=0)
ttk.Label(param_frame, text="Число итераций").grid(row=4, column=0)
ttk.Label(param_frame, text="Задержка (сек)").grid(row=5, column=0)

x_var = tk.DoubleVar()
y_var = tk.DoubleVar()
step_var = tk.DoubleVar()
iterations_var = tk.IntVar()
delay_var = tk.DoubleVar()

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

# Создание панели для отображения результатов
# results_frame = ttk.Frame(root)
# results_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
ttk.Label(param_frame, text="Выполнение и результаты").grid(row=20, column=1)
results_text = tk.Text(param_frame, wrap=tk.WORD, height=10, width=40, state=tk.DISABLED)
results_text.grid(row=21, column=1)

# Инициализация графика при запуске программы
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x_range = np.linspace(-10, 10, 100)
y_range = np.linspace(-10, 10, 100)
X, Y = np.meshgrid(x_range, y_range)
Z = target_function(X, Y)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, padx=20, pady=10)

# Создание панели для параметров функции и ее отображения
# settings_frame = ttk.Frame(root)
# settings_frame.pack(side=tk.TOP, padx=10, pady=10)

ttk.Label(param_frame, text="Функция и отображение ее графика").grid(row=9, column=0)
ttk.Label(param_frame, text="Выберите функцию").grid(row=10, column=0)
function_choices = ["Функция Химмельблау"]
function_var = tk.StringVar(value=function_choices[0])
function_menu = ttk.Combobox(param_frame, textvariable=function_var, values=function_choices)
function_menu.grid(row=10, column=1)
ttk.Label(param_frame, text="X интервал (min)").grid(row=11, column=0)
ttk.Label(param_frame, text="X интервал (max)").grid(row=12, column=0)
ttk.Label(param_frame, text="Y интервал (min)").grid(row=13, column=0)
ttk.Label(param_frame, text="Y интервал (max)").grid(row=14, column=0)
ttk.Label(param_frame, text="Ось X интервал").grid(row=16, column=0)
ttk.Label(param_frame, text="Ось Y интервал").grid(row=17, column=0)

x_interval_min = tk.DoubleVar()
x_interval_max = tk.DoubleVar()
y_interval_min = tk.DoubleVar()
y_interval_max = tk.DoubleVar()
z_scale = tk.DoubleVar()
x_axis_interval = tk.IntVar()
y_axis_interval = tk.IntVar()

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

# Создание кнопки "Применить"
apply_settings_button = ttk.Button(param_frame, text="Выполнить", command=update_function_plot)
apply_settings_button.grid(row=7, column=0, columnspan=2)

root.mainloop()
