class Client:  #Определяем класс Client для клиентов компании
    def __init__(self, name, cargo_weight, is_vip=False):  #Метод инициализации класса
        self.name = name  #Инициализируем атрибут name значением параметра name
        self.cargo_weight = self.validate_cargo_weight(cargo_weight)  #Инициализируем атрибут cargo_weight и валидируем его
        self.is_vip = is_vip  #Инициализируем атрибут is_vip значением параметра is_vip (по умолчанию False)

    def validate_cargo_weight(self, cargo_weight):  #Метод для валидации веса груза
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:  #Проверяем, что вес груза является положительным числом
            raise ValueError("Вес груза должен быть положительным числом")  #Если проверка не пройдена, вызываем исключение ValueError
        return cargo_weight  #Возвращаем валидированный вес груза
