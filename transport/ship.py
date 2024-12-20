from transport.vehicle import Vehicle  #Импортируем класс Vehicle из модуля transport.vehicle

class Ship(Vehicle):  #Определяем класс Ship, который наследует класс Vehicle
    def __init__(self, capacity, name):  #Метод инициализации класса
        super().__init__(capacity)  #Вызываем метод инициализации родительского класса Vehicle
        self.name = name  #Инициализируем атрибут name значением параметра name

    def __str__(self):  #Магический метод __str__ для строкового представления объекта
        return f"Судно {self.name} - {super().__str__()}"  #Возвращаем строку с названием судна и строковым представлением родительского класса Vehicle
