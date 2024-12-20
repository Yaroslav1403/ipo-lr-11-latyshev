import sys  #Импортируем модуль sys для использования функции выхода из программы
from transport.client import Client  #Импортируем класс Client из модуля transport.client
from transport.van import Van  #Импортируем класс Van из модуля transport.van
from transport.ship import Ship  #Импортируем класс Ship из модуля transport.ship
from transport.transportcompany import TransportCompany  #Импортируем класс TransportCompany из модуля transport.transportcompany

def print_menu():  #Функция для отображения меню
    print("Меню:")  #Вывод заголовка меню
    print("1. Добавить клиента")  #Пункт меню для добавления клиента
    print("2. Создать фургон")  #Пункт меню для создания фургона
    print("3. Создать судно")  #Пункт меню для создания судна
    print("4. Загрузить груз в транспортное средство")  #Пункт меню для загрузки груза в транспортное средство
    print("5. Показать информацию о транспортном средстве")  #Пункт меню для отображения информации о транспортном средстве
    print("6. Оптимизировать распределение грузов")  #Пункт меню для оптимизации распределения грузов
    print("7. Выйти")  #Пункт меню для выхода из программы

def main():  #Основная функция программы
    company = TransportCompany("Моя Транспортная Компания")  #Создаем экземпляр класса TransportCompany

    while True:  #Запускаем бесконечный цикл для работы с меню
        print_menu()  #Выводим меню на экран
        choice = input("Выберите пункт меню: ")  #Запрашиваем у пользователя выбор пункта меню

        if choice == '1':  #Если выбран пункт меню 1
            name = input("Введите имя клиента: ")  #Запрашиваем имя клиента
            cargo_weight = float(input("Введите вес груза клиента: "))  #Запрашиваем вес груза клиента
            is_vip = input("Клиент VIP? (да/нет): ").lower() == 'да'  #Запрашиваем, является ли клиент VIP
            client = Client(name, cargo_weight, is_vip)  #Создаем экземпляр класса Client
            company.add_client(client)  #Добавляем клиента в компанию
            print(f"Клиент {name} добавлен.\n")  #Выводим сообщение о добавлении клиента

        elif choice == '2':  #Если выбран пункт меню 2
            capacity = float(input("Введите грузоподъемность фургона (в тоннах): "))  #Запрашиваем грузоподъемность фургона
            is_refrigerated = input("Фургон с холодильником? (да/нет): ").lower() == 'да'  #Запрашиваем, есть ли холодильник у фургона
            van = Van(capacity, is_refrigerated)  #Создаем экземпляр класса Van
            company.add_vehicle(van)  #Добавляем фургон в компанию
            print(f"Фургон создан. ID: {van.vehicle_id}\n")  #Выводим сообщение о создании фургона

        elif choice == '3':  #Если выбран пункт меню 3
            capacity = float(input("Введите грузоподъемность судна (в тоннах): "))  #Запрашиваем грузоподъемность судна
            name = input("Введите название судна: ")  #Запрашиваем название судна
            ship = Ship(capacity, name)  #Создаем экземпляр класса Ship
            company.add_vehicle(ship)  #Добавляем судно в компанию
            print(f"Судно создано. Название: {name}, ID: {ship.vehicle_id}\n")  # Выводим сообщение о создании судна

        elif choice == '4':  #Если выбран пункт меню 4
            client_name = input("Введите имя клиента для загрузки: ")  #Запрашиваем имя клиента
            vehicle_id = input("Введите ID транспортного средства: ")  #Запрашиваем ID транспортного средства

            client = next((c for c in company.clients if c.name == client_name), None)  #Ищем клиента по имени
            vehicle = next((v for v in company.vehicles if v.vehicle_id == vehicle_id), None)  #Ищем транспортное средство по ID

            if client is None:  #Если клиент не найден
                print(f"Клиент с именем {client_name} не найден.\n")  #Выводим сообщение об ошибке
                continue

            if vehicle is None:  #Если транспортное средство не найдено
                print(f"Транспортное средство с ID {vehicle_id} не найдено.\n")  #Выводим сообщение об ошибке
                continue

            try:
                vehicle.load_cargo(client)  #Пытаемся загрузить груз клиента в транспортное средство
            except ValueError as e:  #Обрабатываем ошибку превышения грузоподъемности
                print(f"Ошибка загрузки: {e}\n")
            except TypeError as e:  #Обрабатываем ошибку типа данных
                print(f"Ошибка типа данных: {e}\n")

        elif choice == '5':  #Если выбран пункт меню 5
            if not company.vehicles:  #Если нет транспортных средств
                print("Нет доступных транспортных средств для отображения.\n")  #Выводим сообщение об отсутствии транспортных средств
                continue

            for vehicle in company.vehicles:  #Проходим по всем транспортным средствам
                print(vehicle)  #Выводим информацию о транспортном средстве
                for client in vehicle.clients_list:  #Проходим по всем клиентам, чьи грузы загружены
                    print(f"  - Клиент: {client.name}, Вес груза: {client.cargo_weight} т., VIP: {'Да' if client.is_vip else 'Нет'}")

            print()

        elif choice == '6':  #Если выбран пункт меню 6
            company.optimize_cargo_distribution()  #Оптимизируем распределение грузов
            print("Распределение грузов оптимизировано.\n")

        elif choice == '7':  #Если выбран пункт меню 7
            sys.exit()  #Выход из программы

        else:  #Если выбран неверный пункт меню
            print("Неверный пункт меню, попробуйте снова.\n")  #Выводим сообщение об ошибке

if __name__ == '__main__':  #Проверка, что данный файл запущен напрямую, а не импортирован
    main()  #Вызов основной функции
