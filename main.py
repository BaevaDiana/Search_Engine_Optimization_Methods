import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from LR1 import GradientDescentAlgorithm
from LR2 import Simplex_method
from LR3.LR3 import GeneticAlgorithm
from LR4.particleswarm.LR4 import ParticleSwarmAlgorithm
from LR5.LR5 import BeesAlgorithm
from LR6 import ImmuneAlgorithm
from LR7 import BFO
from LR8 import PSO


# Создание окна приложения
root = tk.Tk()
root.title("Методы поисковой оптимизации")

notebook = ttk.Notebook(root)
notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Инициализация графика при запуске программы
fig = plt.figure(figsize=(8, 9))  # Установка размеров фигуры (ширина, высота)
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT, padx=20)

# Вкладка для лр1
param_frame = ttk.Frame(notebook,padding=(15, 0))
notebook.add(param_frame, text="ЛР1")
GradientDescentAlgorithm(param_frame,root,ax,canvas)
# Вкладка для лр2
param_frame2 = ttk.Frame(notebook)
notebook.add(param_frame2, text="ЛР2")
Simplex_method(param_frame2,root,ax,canvas)
# Вкладка для лр3
param_frame3 = ttk.Frame(notebook)
notebook.add(param_frame3, text="ЛР3")
GeneticAlgorithm(param_frame3,root,ax,canvas)
# Вкладка для лр4
param_frame4 = ttk.Frame(notebook)
notebook.add(param_frame4, text="ЛР4")
ParticleSwarmAlgorithm(param_frame4,root,ax,canvas)
# Вкладка для лр5
param_frame5 = ttk.Frame(notebook)
notebook.add(param_frame5, text="ЛР5")
BeesAlgorithm(param_frame5,root,ax,canvas)
# Вкладка для лр6
param_frame6 = ttk.Frame(notebook)
notebook.add(param_frame6, text="ЛР6")
ImmuneAlgorithm(param_frame6,root,ax,canvas)

param_frame7 = ttk.Frame(notebook)
notebook.add(param_frame7, text="ЛР7")
BFO(param_frame7,root,ax,canvas)

param_frame8 = ttk.Frame(notebook)
notebook.add(param_frame8, text="ЛР8")
PSO(param_frame8,root,ax,canvas)

root.mainloop()
