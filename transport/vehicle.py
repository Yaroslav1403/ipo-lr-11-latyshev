import uuid  #Импортируем модуль uuid для генерации уникальных идентификаторов
from transport.client import Client  #Импортируем класс Client из модуля transport.client

class Vehicle:  #Определяем класс Vehicle для транспортного средства
    def __init__(self, capacity):  #Метод инициализации класса
        self.vehicle_id = str(uuid.uuid4())  #Генерация уникального идентификатора транспортного средства
        self.capacity = self.validate_capacity(capacity)  #Валидация и установка грузоподъемности
        self.current_load = 0  #Инициализация текущей загрузки (по умолчанию 0)
        self.clients_list = []  #Инициализация списка клиентов, чьи грузы загружены

    def validate_capacity(self, capacity):  #Метод для валидации грузоподъемности
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом")
        return capacity  #Возвращаем валидированную грузоподъемность

    def load_cargo(self, client):  #Метод для загрузки груза клиента в транспортное средство
        if not isinstance(client, Client):  #Проверка, что переданный объект является экземпляром класса Client
            raise TypeError("Ожидается объект класса Client")
        
        if self.current_load + client.cargo_weight > self.capacity:  #Проверка на превышение грузоподъемности
            raise ValueError("Превышение грузоподъемности")
        
        self.current_load += client.cargo_weight  #Увеличение текущей загрузки на вес груза клиента
        self.clients_list.append(client)  #Добавление клиента в список загруженных клиентов
        print(f"Груз клиента {client.name} весом {client.cargo_weight} т. загружен.")  #Вывод сообщения о загрузке груза

    def __str__(self):  #Магический метод __str__ для строкового представления транспортного средства
        return f"ID транспортного средства: {self.vehicle_id}, Грузоподъемность: {self.capacity} т., Текущая загрузка = {self.current_load} т."
