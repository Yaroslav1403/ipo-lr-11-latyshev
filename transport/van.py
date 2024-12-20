from transport.vehicle import Vehicle  #Импортируем класс Vehicle из модуля transport.vehicle

class Van(Vehicle):  #Определяем класс Van, который наследует класс Vehicle
    def __init__(self, capacity, is_refrigerated=False):  #Метод инициализации класса
        super().__init__(capacity)  #Вызываем метод инициализации родительского класса Vehicle
        self.is_refrigerated = is_refrigerated  #Инициализируем атрибут is_refrigerated значением параметра is_refrigerated (по умолчанию False)
