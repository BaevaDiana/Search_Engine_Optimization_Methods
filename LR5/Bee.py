

# Класс для представления пчелы
class Bee:
    """
     coords - координаты поля для пчелы
     fitness - значение фитнесс-функции для центра данного участка
    """
    def __init__(self, coords, fitness):
        self.coords = coords
        self.fitness = fitness