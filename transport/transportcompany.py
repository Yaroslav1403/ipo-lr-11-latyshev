from transport.client import Client  #Импортируем класс Client из модуля transport.client
from transport.vehicle import Vehicle  #Импортируем класс Vehicle из модуля transport.vehicle

class TransportCompany:  #Определяем класс TransportCompany для транспортной компании
    def __init__(self, name):  #Метод инициализации класса
        self.name = name  #Инициализируем атрибут name значением параметра name
        self.vehicles = []  #Инициализируем список транспортных средств
        self.clients = []  #Инициализируем список клиентов

    def add_vehicle(self, vehicle):  #Метод для добавления транспортного средства
        if not isinstance(vehicle, Vehicle):  #Проверка, что переданный объект является экземпляром класса Vehicle
            raise TypeError("Ожидается объект класса Vehicle")
        self.vehicles.append(vehicle)  #Добавление транспортного средства в список

    def list_vehicles(self):  #Метод для возврата списка всех транспортных средств
        return self.vehicles  #Возвращаем список транспортных средств

    def add_client(self, client):  #Метод для добавления клиента
        if not isinstance(client, Client):  #Проверка, что переданный объект является экземпляром класса Client
            raise TypeError("Ожидается объект класса Client")
        self.clients.append(client)  #Добавление клиента в список

    def optimize_cargo_distribution(self):  #Метод для оптимизации распределения грузов
        self.clients.sort(key=lambda x: (-x.is_vip, x.cargo_weight))  #Сортировка клиентов: сначала VIP, затем по весу груза
        for client in self.clients:  #Проходим по каждому клиенту
            for vehicle in self.vehicles:  #Проходим по каждому транспортному средству
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:  #Проверяем, может ли транспортное средство принять груз клиента
                    vehicle.load_cargo(client)  #Загружаем груз клиента в транспортное средство
                    break  #Выходим из внутреннего цикла, если груз загружен
