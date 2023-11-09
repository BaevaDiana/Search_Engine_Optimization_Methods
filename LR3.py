import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import numpy as np


def GeneticAlgorithm(frame,root,ax,canvas):

        # Функция Розенброка для оптимизации
        def rosenbrock_function(x, y):
            return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

        # Оператор селекции (выбор лучших особей)
        def selection(population, fitness_scores):
            # Выбираем двух наилучших особей
            best_indices = np.argsort(fitness_scores)[:2]
            return [population[i] for i in best_indices]

        # Оператор кроссовера (одноточечный кроссовер)
        def crossover(parent1, parent2):
            crossover_point = np.random.randint(1, len(parent1))
            child = np.hstack((parent1[:crossover_point], parent2[crossover_point:]))
            return child

        # Оператор мутации
        def mutate(individual, mutation_rate):
            mutation_indices = np.random.rand(len(individual)) < mutation_rate
            individual[mutation_indices] += np.random.uniform(-0.5, 0.5)
            return individual


        def run_optimization():
            # Генерация сетки для графика целевой функции
            x_range = np.linspace(x_interval_min.get(), x_interval_max.get(), 100)
            y_range = np.linspace(y_interval_min.get(), y_interval_max.get(), 100)
            X, Y = np.meshgrid(x_range, y_range)
            Z = rosenbrock_function(X, Y)

            population_size=int(x_var.get())
            num_generations=int(y_var.get())
            #рандомно задаем популяцию от -5 до 5
            population = np.random.uniform(low=-5, high=5, size=(population_size, 2))

            #для записи результатов
            results = []
            results_text.config(state=tk.NORMAL)
            results_text.delete(1.0, tk.END)
            for generation in range(num_generations):
                # Расчет значений функции для текущей популяции
                fitness_scores = np.array([rosenbrock_function(x, y) for x, y in population])

                # Выбор лучших особей
                selected_individuals = selection(population, fitness_scores)

                # Оператор кроссовера и мутации
                children = []
                for i in range(0, population_size, 2):
                    child1 = crossover(selected_individuals[0], selected_individuals[1])
                    child2 = crossover(selected_individuals[1], selected_individuals[0])
                    child1 = mutate(child1, mutation_rate=0.1)  # Пример вероятности мутации
                    child2 = mutate(child2, mutation_rate=0.1)
                    children.extend([child1, child2])

                ax.cla()
                # Построение поверхности графика целевой функции
                ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xticks(np.arange(x_interval_min.get(), x_interval_max.get() + 1, x_axis_interval.get()))
                ax.set_yticks(np.arange(y_interval_min.get(), y_interval_max.get() + 1, y_axis_interval.get()))
                ax.set_title("Генетический алгоритм")

                for i in range(len(fitness_scores)):
                    best_individual = population[i]
                    ax.scatter(best_individual[0], best_individual[1], fitness_scores[i], color='red',
                               s=10)

                # Обновление популяции
                population = np.array(children)

                # Нахождение лучшей особи на текущей итерации
                best_fitness = np.min(fitness_scores)
                best_individual = population[np.argmin(fitness_scores)]

                # Вывод лучшего решения на текущей итерации
                print(f"Поколение {generation}: Лучшее решение - {best_individual}, Значение функции - {best_fitness}")

                results.append((best_individual[0], best_individual[1], generation, best_fitness))
                results_text.insert(tk.END,
                                    f"Поколение {generation}: Лучшее решение ({best_individual[0]:.2f}, {best_individual[1]:.2f}), Значение функции: {best_fitness:.7f}\n")
                results_text.yview_moveto(1)
                canvas.draw()
                root.update()


            # Нахождение лучшего решения после всех итераций
            final_fitness_scores = np.array([rosenbrock_function(x, y) for x, y in population])
            best_index = np.argmin(final_fitness_scores)
            best_solution = population[best_index]
            best_fitness_value = final_fitness_scores[best_index]

            results_text.insert(tk.END,
                                f"\nОптимизация завершена. Лучшее решение - {best_solution}, Значение функции - {best_fitness_value}")
            results_text.yview_moveto(1)
            ax.scatter(best_solution[0], best_solution[1], best_fitness_value, color='black', marker='x', s=60)
            results_text.config(state=tk.DISABLED)


        param_frame2 = frame

        # Параметры задачи
        ttk.Label(param_frame2, text="Инициализация значений", font=("Helvetica", 12)).grid(row=0, column=0, pady=15)
        ttk.Label(param_frame2, text="Особи", font=("Helvetica", 10)).grid(row=1, column=0)
        ttk.Label(param_frame2, text="Итерации", font=("Helvetica", 10)).grid(row=2, column=0)


        x_var = tk.DoubleVar(value=100)
        y_var = tk.DoubleVar(value=100)
        x_entry = ttk.Entry(param_frame2, textvariable=x_var)
        y_entry = ttk.Entry(param_frame2, textvariable=y_var)

        x_entry.grid(row=1, column=1)
        y_entry.grid(row=2, column=1)


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

