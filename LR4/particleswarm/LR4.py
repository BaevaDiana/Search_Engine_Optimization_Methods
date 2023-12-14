import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np
import math
from LR4.particleswarm.swarm import Swarm
import numpy


class Swarm_Rastrigin (Swarm):
    def __init__ (self,
            swarmsize,
            minvalues,
            maxvalues,
            currentVelocityRatio,
            localVelocityRatio,
            globalVelocityRatio):
       Swarm.__init__ (self,
            swarmsize,
            minvalues,
            maxvalues,
            currentVelocityRatio,
            localVelocityRatio,
            globalVelocityRatio)


    def _finalFunc (self, position):
        function = 10.0 * len (self.minvalues) + sum (position * position - 10.0 * numpy.cos (2 * numpy.pi * position) )
        penalty = self._getPenalty (position, 10000.0)

        return function + penalty



# инерция
# альфа
# бетта

def printResult (swarm, iteration):
    template = u""" Лучшие координаты: {bestpos}\n Лучший результат: {finalfunc}\n\n"""

    result = template.format (iter = iteration,
            bestpos = swarm.globalBestPosition,
            finalfunc = swarm.globalBestFinalFunc)

    return result


def ParticleSwarmAlgorithm(frame,root,ax,canvas):

        def rastrigin(*X):
            A = 10
            return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])

        def run_optimization():
            # Генерация сетки для графика целевой функции
            X = np.linspace(x_interval_min.get(), x_interval_max.get(), 200)
            Y = np.linspace(y_interval_min.get(), y_interval_max.get(), 200)

            X, Y = np.meshgrid(X, Y)
            Z = rastrigin(X, Y)


            iterCount = iteration.get()
            dimension = 3
            swarmsize = particle.get()
            minvalues = numpy.array ([-5.12] * dimension)
            maxvalues = numpy.array ([5.12] * dimension)

            currentVelocityRatio = inertia.get()
            localVelocityRatio = alpha.get()
            globalVelocityRatio = beta.get()

            swarm = Swarm_Rastrigin(swarmsize,
                                    minvalues,
                                    maxvalues,
                                    currentVelocityRatio,
                                    localVelocityRatio,
                                    globalVelocityRatio
                                    )


            #для записи результатов
            results = []
            results_text.config(state=tk.NORMAL)
            results_text.delete(1.0, tk.END)

            for n in range(iterCount):
                ax.cla()
                # Построение поверхности графика целевой функции
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.5)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xticks(np.arange(x_interval_min.get(), x_interval_max.get() + 1, x_axis_interval.get()))
                ax.set_yticks(np.arange(y_interval_min.get(), y_interval_max.get() + 1, y_axis_interval.get()))
                ax.set_title("Алгоритм Роя Частиц")

                ax.scatter(swarm[0].position[0], swarm[0].position[1], swarm[0].position[2], color='red',
                               s=10)

                results_text.insert(tk.END,
                                    f"Итерация {n}\n")

                results_text.insert(tk.END,
                                    f"Позиция {swarm[0].position}\n")
                results_text.insert(tk.END,
                                    f"Скорость {swarm[0].velocity}\n")



                results_text.insert(tk.END,printResult(swarm, n))
                swarm.nextIteration()
                results_text.yview_moveto(1)
                canvas.draw()
                root.update()


        param_frame2 = frame

        # Параметры задачи
        ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
        ttk.Label(param_frame2, text="Частиц", font=("Helvetica", 10)).grid(row=2, column=0)
        ttk.Label(param_frame2, text="Итераций", font=("Helvetica", 10)).grid(row=1, column=0)
        ttk.Label(param_frame2, text="Альфа", font=("Helvetica", 10)).grid(row=3, column=0)
        ttk.Label(param_frame2, text="Бета", font=("Helvetica", 10)).grid(row=4, column=0)
        ttk.Label(param_frame2, text="Инерция", font=("Helvetica", 10)).grid(row=5, column=0)

        #частиц
        particle = tk.IntVar(value=2000)
        iteration = tk.IntVar(value=100)
        alpha=tk.IntVar(value=2)
        beta=tk.IntVar(value=5)
        inertia=tk.DoubleVar(value=0.5)

        particle_entry = ttk.Entry(param_frame2, textvariable=particle)
        iteration_entry = ttk.Entry(param_frame2, textvariable=iteration)
        alpha_entry = ttk.Entry(param_frame2, textvariable=alpha)
        beta_entry = ttk.Entry(param_frame2, textvariable=beta)
        inertia_entry = ttk.Entry(param_frame2, textvariable=inertia)

        particle_entry.grid(row=2, column=1)
        iteration_entry.grid(row=1, column=1)
        alpha_entry.grid(row=3, column=1)
        beta_entry.grid(row=4, column=1)
        inertia_entry.grid(row=5, column=1)


        separator = ttk.Separator(param_frame2, orient="horizontal")  # Горизонтальная полоса разделения
        separator.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

        # Параметры функции
        ttk.Label(param_frame2, text="Функция и отображение ее графика", font=("Helvetica", 12)).grid(row=9, column=0, pady=10)
        ttk.Label(param_frame2, text="Выберите функцию", font=("Helvetica", 10)).grid(row=10, column=0)
        function_choices = ["Функция Растригина"]
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

        x_interval_min = tk.DoubleVar(value=-4)
        x_interval_max = tk.DoubleVar(value=4)
        y_interval_min = tk.DoubleVar(value=-4)
        y_interval_max = tk.DoubleVar(value=4)
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
        # root.mainloop()

