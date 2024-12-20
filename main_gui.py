import tkinter as tk  #Импортируем библиотеку tkinter для создания графического интерфейса
from tkinter import messagebox, ttk, filedialog  #Импортируем дополнительные модули для работы с окнами сообщений, таблицами и диалогами
import re  #Импортируем библиотеку для работы с регулярными выражениями

#Класс для представления клиента
class Client:
    def __init__(self, name, cargo_weight, vip_status):
        self.name = name  # Имя клиента
        self.cargo_weight = cargo_weight  #Вес груза клиента
        self.vip_status = vip_status  #VIP статус клиента (Да/Нет)

#Класс для представления транспортного средства
class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, capacity, is_refrigerated = None, name = None):
        self.vehicle_id = vehicle_id  #ID транспортного средства
        self.vehicle_type = vehicle_type  #Тип транспортного средства (Фургон/Судно)
        self.capacity = capacity  #Грузоподъемность
        self.is_refrigerated = is_refrigerated  #Холодильник (для фургонов)
        self.name = name  #Название судна (для судов)

#Класс для управления транспортной компанией
class TransportCompany:
    def __init__(self):
        self.clients = []  #Список клиентов
        self.vehicles = []  #Список транспортных средств

    def add_client(self, client):
        self.clients.append(client)  #Добавление клиента в список

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)  #Добавление транспортного средства в список

    def remove_client(self, client_name):
        #Удаление клиента по имени
        self.clients = [client for client in self.clients if client.name != client_name]

    def remove_vehicle(self, vehicle_id):
        #Удаление транспортного средства по ID
        self.vehicles = [vehicle for vehicle in self.vehicles if vehicle.vehicle_id != vehicle_id]

#Основной класс приложения
class TransportApp:
    def __init__(self, master):
        self.master = master  #Сохраняем ссылку на главное окно
        self.master.title("Моя транспортная компания")  #Устанавливаем заголовок окна
        
        self.company = TransportCompany()  #Создаем объект транспортной компании
        
        #Создаем меню
        self.menu = tk.Menu(self.master)  #Создаем меню
        self.master.config(menu = self.menu)  #Применяем меню к главному окну
        self.menu.add_command(label = "Экспорт результата", command = self.export_results)  #Добавляем команду для экспорта
        self.menu.add_command(label = "О программе", command = self.show_about)  #Добавляем команду "О программе"

        # Рабочая область
        self.control_frame = tk.Frame(self.master)  #Создаем фрейм для управления
        self.control_frame.pack()  #Упаковываем фрейм

        #Таблицы для отображения клиентов и транспортных средств
        self.client_table = ttk.Treeview(self.control_frame, columns = ('Имя', 'Вес груза', 'VIP статус'))  #Таблица клиентов
        self.client_table.heading('#0', text = 'ID')  #Заголовок для ID
        self.client_table.heading('Имя', text = 'Имя клиента')  #Заголовок для имени клиента
        self.client_table.heading('Вес груза', text = 'Вес груза')  #Заголовок для веса груза
        self.client_table.heading('VIP статус', text = 'VIP статус')  #Заголовок для VIP статуса
        self.client_table.pack(side = tk.LEFT)  #Упаковываем таблицу

        self.vehicle_table = ttk.Treeview(self.control_frame, columns = ('Тип', 'Грузоподъемность', 'Холодильник/Название'))  #Таблица транспортных средств
        self.vehicle_table.heading('#0', text = 'ID')  #Заголовок для ID
        self.vehicle_table.heading('Тип', text = 'Тип транспорта')  #Заголовок для типа транспорта
        self.vehicle_table.heading('Грузоподъемность', text = 'Грузоподъемность')  #Заголовок для грузоподъемности
        self.vehicle_table.heading('Холодильник/Название', text = 'Холодильник/Название')  #Заголовок для холодильника или названия
        self.vehicle_table.pack(side = tk.LEFT)  #Упаковываем таблицу

        #Панель с кнопками
        self.button_frame = tk.Frame(self.master)  #Создаем фрейм для кнопок
        self.button_frame.pack()  #Упаковываем фрейм

        #Кнопки для добавления клиентов и транспортных средств, распределения грузов и удаления
        self.add_client_button = tk.Button(self.button_frame, text = "Добавить клиента", command = self.open_client_window)  #Кнопка для добавления клиента
        self.add_client_button.pack(side = tk.LEFT)  #Упаковываем кнопку

        self.add_vehicle_button = tk.Button(self.button_frame, text = "Добавить транспорт", command = self.open_vehicle_window)  #Кнопка для добавления транспортного средства
        self.add_vehicle_button.pack(side = tk.LEFT)  #Упаковываем кнопку

        self.distribute_button = tk.Button(self.button_frame, text = "Распределить грузы", command = self.distribute_cargo)  #Кнопка для распределения грузов
        self.distribute_button.pack(side = tk.LEFT)  #Упаковываем кнопку

        self.delete_client_button = tk.Button(self.button_frame, text = "Удалить клиента", command = self.delete_selected_client)  #Кнопка для удаления клиента
        self.delete_client_button.pack(side = tk.LEFT)  #Упаковываем кнопку

        self.delete_vehicle_button = tk.Button(self.button_frame, text = "Удалить транспорт", command = self.delete_selected_vehicle)  #Кнопка для удаления транспортного средства
        self.delete_vehicle_button.pack(side = tk.LEFT)  #Упаковываем кнопку

        #Строка состояния
        self.status = tk.StringVar()  #Создаем строку состояния
        self.status_label = tk.Label(self.master, textvariable = self.status)  #Создаем метку для отображения статуса
        self.status_label.pack()  #Упаковываем метку

        #Привязка клавиш к действиям
        self.master.bind('<Return>', lambda event: self.add_client_button.invoke())  #Привязка клавиши Enter к добавлению клиента
        self.master.bind('<Escape>', lambda event: self.master.quit())  #Привязка клавиши Escape для выхода

        self.create_tooltips()  #Создаем подсказки для кнопок

    def create_tooltips(self):
        #Создание подсказок для кнопок
        self.add_tooltip(self.add_client_button, "Добавить нового клиента")  #Подсказка для кнопки добавления клиента
        self.add_tooltip(self.add_vehicle_button, "Добавить новое транспортное средство")  #Подсказка для кнопки добавления транспорта
        self.add_tooltip(self.delete_client_button, "Удалить выбранного клиента")  #Подсказка для кнопки удаления клиента
        self.add_tooltip(self.delete_vehicle_button, "Удалить выбранное транспортное средство")  #Подсказка для кнопки удаления транспорта
        self.add_tooltip(self.distribute_button, "Распределить грузы между транспортными средствами")  #Подсказка для кнопки распределения грузов

    def add_tooltip(self, widget, text):
        # Функция для создания подсказки
        tooltip = tk.Toplevel(self.master)  #Создаем новое окно для подсказки
        tooltip.wm_overrideredirect(True)  #Убираем рамку окна
        tooltip.withdraw()  #Скрываем подсказку
        tooltip_label = tk.Label(tooltip, text = text, bg = "lightyellow", borderwidth = 1, relief = "solid")  #Создаем метку для подсказки
        tooltip_label.pack()  #Упаковываем метку

        def show_tooltip(event):
            #Показываем подсказку
            x = event.x_root + 10  #Устанавливаем координату X
            y = event.y_root + 10  #Устанавливаем координату Y
            tooltip.wm_geometry(f"+{x}+{y}")  #Устанавливаем позицию подсказки
            tooltip.deiconify()  #Показываем подсказку

        def hide_tooltip(event):
            #Скрываем подсказку
            tooltip.withdraw()  #Скрываем подсказку

        widget.bind("<Enter>", show_tooltip)  #При наведении показываем подсказку
        widget.bind("<Leave>", hide_tooltip)  #При уходе скрываем подсказку

    def open_client_window(self):
        #Открытие окна для добавления клиента
        self.client_window = tk.Toplevel(self.master)  #Создаем новое окно
        self.client_window.title("Добавить клиента")  #Устанавливаем заголовок окна

        tk.Label(self.client_window, text = "Имя клиента:").grid(row=0, column=0)  #Метка для имени клиента
        self.client_name_entry = tk.Entry(self.client_window)  #Поле ввода для имени клиента
        self.client_name_entry.grid(row = 0, column = 1)  #Устанавливаем позицию поля ввода

        tk.Label(self.client_window, text = "Вес груза:").grid(row = 1, column = 0)  #Метка для веса груза
        self.cargo_weight_entry = tk.Entry(self.client_window)  #Поле ввода для веса груза
        self.cargo_weight_entry.grid(row = 1, column = 1)  #Устанавливаем позицию поля ввода

        self.vip_status_var = tk.BooleanVar()  #Переменная для VIP статуса
        tk.Checkbutton(self.client_window, text = "VIP статус", variable = self.vip_status_var).grid(row = 2, columnspan = 2)  #Чекбокс для VIP статуса
        tk.Button(self.client_window, text = "Сохранить", command = self.save_client).grid(row = 3, column = 0)  #Кнопка для сохранения клиента
        tk.Button(self.client_window, text = "Отмена", command = self.client_window.destroy).grid(row = 3, column = 1)  #Кнопка для отмены

    def save_client(self):
        #Сохранение данных клиента
        name = self.client_name_entry.get()  #Получаем имя клиента
        cargo_weight = self.cargo_weight_entry.get()  #Получаем вес груза
        vip_status = self.vip_status_var.get()  #Получаем VIP статус

        if not self.validate_client_data(name, cargo_weight):  #Валидация данных клиента
            return  #Если данные невалидны, выходим

        if not self.check_cargo_weight_against_capacity(float(cargo_weight)):  #Проверка на превышение грузоподъемности
            return  #Если превышает, выходим

        client = Client(name, float(cargo_weight), vip_status)  #Создаем объект клиента
        self.company.add_client(client)  #Добавляем клиента в компанию
        self.update_client_table()  #Обновляем таблицу клиентов
        self.client_window.destroy()  #Закрываем окно
        self.status.set(f"Клиент {name} добавлен.")  #Обновляем статус

    def validate_client_data(self, name, cargo_weight):
        #Валидация данных клиента
        if not re.match("^[A-Za-zА-Яа-яЁё ]{2,}$", name):  #Проверка имени клиента
            messagebox.showwarning("Ошибка", "Имя клиента должно содержать только буквы и минимум 2 символа.")  #Сообщение об ошибке
            return False  #Возвращаем False, если имя невалидно
        if not cargo_weight.isdigit() or float(cargo_weight) <= 0 or float(cargo_weight) > 10000:  #Проверка веса груза
            messagebox.showwarning("Ошибка", "Вес груза должен быть положительным числом и не более 10000 кг.")  #Сообщение об ошибке
            return False  #Возвращаем False, если вес невалиден
        return True  #Возвращаем True, если данные валидны

    def check_cargo_weight_against_capacity(self, cargo_weight):
        #Проверка на превышение грузоподъемности
        available_capacity = sum(vehicle.capacity for vehicle in self.company.vehicles)  #Общая грузоподъемность
        if cargo_weight > available_capacity:  #Если вес груза превышает грузоподъемность
            messagebox.showwarning("Ошибка", "Вес груза превышает общую грузоподъемность доступных транспортных средств.")  #Сообщение об ошибке
            return False  #Возвращаем False
        return True  #Возвращаем True, если все в порядке

    def open_vehicle_window(self):
        #Открытие окна для добавления транспортного средства
        self.vehicle_window = tk.Toplevel(self.master)  #Создаем новое окно
        self.vehicle_window.title("Добавить транспорт")  #Устанавливаем заголовок окна

        tk.Label(self.vehicle_window, text = "Тип транспорта:").grid(row = 0, column = 0)  #Метка для типа транспорта
        self.vehicle_type_var = tk.StringVar()  #Переменная для типа транспорта
        self.vehicle_type_combobox = ttk.Combobox(self.vehicle_window, textvariable = self.vehicle_type_var, values = ["Фургон", "Судно"])  #Комбобокс для выбора типа
        self.vehicle_type_combobox.grid(row = 0, column = 1)  #Устанавливаем позицию комбобокса

        tk.Label(self.vehicle_window, text = "Грузоподъемность:").grid(row = 1, column = 0)  #Метка для грузоподъемности
        self.capacity_entry = tk.Entry(self.vehicle_window)  #Поле ввода для грузоподъемности
        self.capacity_entry.grid(row = 1, column = 1)  #Устанавливаем позицию поля ввода

        #Дополнительные поля в зависимости от типа транспорта
        self.is_refrigerated_var = tk.BooleanVar()  #Переменная для холодильника
        self.refrigerated_label = tk.Label(self.vehicle_window, text = "Холодильник:")  #Метка для холодильника
        self.refrigerated_checkbutton = tk.Checkbutton(self.vehicle_window, variable = self.is_refrigerated_var)  #Чекбокс для холодильника
        
        self.name_label = tk.Label(self.vehicle_window, text="Название судна:")  #Метка для названия судна
        self.name_entry = tk.Entry(self.vehicle_window)  #Поле ввода для названия судна

        self.vehicle_type_combobox.bind("<<ComboboxSelected>>", self.update_vehicle_fields)  #Привязка события выбора типа

        tk.Button(self.vehicle_window, text = "Сохранить", command = self.save_vehicle).grid(row = 4, column = 0)  #Кнопка для сохранения транспортного средства
        tk.Button(self.vehicle_window, text = "Отмена", command = self.vehicle_window.destroy).grid(row = 4, column = 1)  #Кнопка для отмены

    def update_vehicle_fields(self, event):
        #Обновление полей в зависимости от выбранного типа транспорта
        vehicle_type = self.vehicle_type_var.get()  #Получаем выбранный тип транспорта
        if vehicle_type == "Фургон":  #Если выбран фургон
            self.refrigerated_label.grid(row = 3, column = 0)  #Показываем метку для холодильника
            self.refrigerated_checkbutton.grid(row = 3, column = 1)  #Показываем чекбокс для холодильника
            self.name_label.grid_forget()  #Скрываем метку для названия
            self.name_entry.grid_forget()  #Скрываем поле ввода для названия
        elif vehicle_type == "Судно":  #Если выбран судно
            self.refrigerated_label.grid_forget()  #Скрываем метку для холодильника
            self.refrigerated_checkbutton.grid_forget()  #Скрываем чекбокс для холодильника
            self.name_label.grid(row = 3, column = 0)  #Показываем метку для названия судна
            self.name_entry.grid(row = 3, column = 1)  #Показываем поле ввода для названия судна

    def save_vehicle(self):
        #Сохранение данных транспортного средства
        vehicle_type = self.vehicle_type_var.get()  #Получаем тип транспорта
        capacity = self.capacity_entry.get()  #Получаем грузоподъемность
        
        #Получаем дополнительные данные в зависимости от типа транспорта
        is_refrigerated = self.is_refrigerated_var.get() if vehicle_type == "Фургон" else None  #Холодильник для фургона
        name = self.name_entry.get() if vehicle_type == "Судно" else None  #Название для судна

        if not self.validate_vehicle_data(vehicle_type, capacity, is_refrigerated, name):  #Валидация данных транспортного средства
            return  #Если данные невалидны, выходим

        vehicle_id = len(self.company.vehicles) + 1  #Генерация ID для нового транспортного средства
        vehicle = Vehicle(vehicle_id, vehicle_type, float(capacity), is_refrigerated, name)  #Создаем объект транспортного средства
        self.company.add_vehicle(vehicle)  #Добавляем транспортное средство в компанию
        self.update_vehicle_table()  #Обновляем таблицу транспортных средств
        self.vehicle_window.destroy()  #Закрываем окно
        self.status.set(f"Транспортное средство {vehicle_type} добавлено.")  #Обновляем статус

    def validate_vehicle_data(self, vehicle_type, capacity, is_refrigerated, name):
        #Валидация данных транспортного средства
        if vehicle_type not in ["Фургон", "Судно"]:  #Проверка типа транспорта
            messagebox.showwarning("Ошибка", "Выберите корректный тип транспорта.")  #Сообщение об ошибке
            return False  #Возвращаем False
        if not capacity.isdigit() or float(capacity) <= 0:  #Проверка грузоподъемности
            messagebox.showwarning("Ошибка", "Грузоподъемность должна быть положительным числом.")  #Сообщение об ошибке
            return False  #Возвращаем False
        if vehicle_type == "Судно" and not name:  #Проверка на название судна
            messagebox.showwarning("Ошибка", "Введите название судна.")  #Сообщение об ошибке
            return False  #Возвращаем False
        return True  #Возвращаем True, если данные валидны

    def update_client_table(self):
        #Обновление таблицы клиентов
        for item in self.client_table.get_children():  #Удаляем старые данные
            self.client_table.delete(item)
        for index, client in enumerate(self.company.clients):  #Перебираем клиентов
            vip_status = "Да" if client.vip_status else "Нет"  #Определяем VIP статус
            self.client_table.insert('', 'end', text=index + 1, values=(client.name, client.cargo_weight, vip_status))  #Добавляем клиента в таблицу

    def update_vehicle_table(self):
        #Обновление таблицы транспортных средств
        for item in self.vehicle_table.get_children():  #Удаляем старые данные
            self.vehicle_table.delete(item)
        for index, vehicle in enumerate(self.company.vehicles):  #Перебираем транспортные средства
            vehicle_info = vehicle.is_refrigerated if vehicle.vehicle_type == "Фургон" else vehicle.name  #Получаем информацию о транспортном средстве
            if vehicle.vehicle_type == "Фургон":  #Если это фургон
                vehicle_info = "Да" if vehicle.is_refrigerated else "Нет"  #Определяем наличие холодильника
            self.vehicle_table.insert('', 'end', text=index + 1, values=(vehicle.vehicle_type, vehicle.capacity, vehicle_info))  #Добавляем транспортное средство в таблицу

    def delete_selected_client(self):
        #Удаление выбранного клиента
        selected_item = self.client_table.selection()  #Получаем выбранный элемент
        if selected_item:  #Если элемент выбран
            client_name = self.client_table.item(selected_item)['values'][0]  #Получаем имя клиента
            self.company.remove_client(client_name)  #Удаляем клиента из компании
            self.update_client_table()  #Обновляем таблицу
            self.status.set(f"Клиент {client_name} удален.")  #Обновляем статус

    def delete_selected_vehicle(self):
        #Удаление выбранного транспортного средства
        selected_item = self.vehicle_table.selection()  #Получаем выбранный элемент
        if selected_item:  #Если элемент выбран
            vehicle_id = self.vehicle_table.item(selected_item)['text']  #Получаем ID транспортного средства
            self.company.remove_vehicle(vehicle_id)  #Удаляем транспортное средство из компании
            self.update_vehicle_table()  #Обновляем таблицу
            self.status.set(f"Транспортное средство {vehicle_id} удалено.")  #Обновляем статус

    def distribute_cargo(self):
        #Распределение грузов между транспортными средствами
        distribution_results = self.optimize_cargo_distribution()  #Оптимизация распределения грузов
        self.show_distribution_results(distribution_results)  #Отображение результатов распределения

    def optimize_cargo_distribution(self):
        #Оптимизация распределения грузов
        results = []  #Список для хранения результатов
        total_cargo = sum(client.cargo_weight for client in self.company.clients)  #Общий вес грузов
        available_vehicles = self.company.vehicles  #Доступные транспортные средства
        for vehicle in available_vehicles:  #Перебираем доступные транспортные средства
            if total_cargo > 0:  #Если есть грузы для распределения
                load = min(vehicle.capacity, total_cargo)  #Максимально возможная загрузка
                total_cargo -= load  #Уменьшаем оставшийся вес
                results.append((vehicle.vehicle_type, load))  #Сохраняем результаты
        return results  #Возвращаем результаты распределения

    def show_distribution_results(self, results):
        #Отображение результатов распределения грузов
        result_window = tk.Toplevel(self.master)  #Создаем новое окно для результатов
        #Устанавливаем заголовок для окна результатов распределения грузов
        result_window.title("Результаты распределения грузов")
        #Создаем таблицу (Treeview) для отображения результатов с двумя колонками: 'Тип транспорта' и 'Загруженный вес'
        result_table = ttk.Treeview(result_window, columns  =('Тип транспорта', 'Загруженный вес'))
        #Устанавливаем заголовок для первой колонки (по умолчанию это колонка с ID)
        result_table.heading('#0', text='ID')
        #Устанавливаем заголовок для колонки 'Тип транспорта'
        result_table.heading('Тип транспорта', text = 'Тип транспорта')
        #Устанавливаем заголовок для колонки 'Загруженный вес'
        result_table.heading('Загруженный вес', text = 'Загруженный вес')
        #Добавляем таблицу в окно результатов
        result_table.pack()

        #Заполняем таблицу результатами, проходя по каждому элементу в results
        for index, (vehicle_type, load) in enumerate(results):
            #Вставляем новую строку в таблицу с индексом и значениями типа транспорта и загруженного веса
            result_table.insert('', 'end', text = index + 1, values = (vehicle_type, load))
        #Создаем кнопку "Закрыть", которая закрывает окно результатов при нажатии
        tk.Button(result_window, text = "Закрыть", command=result_window.destroy).pack()

    def export_results(self):
        #Проверяем, есть ли данные для экспорта (клиенты и транспортные средства)
        if not self.company.clients and not self.company.vehicles:
            #Если данных нет, показываем предупреждение
            messagebox.showwarning("Ошибка", "Нет данных для экспорта.")
            return

        #Открываем диалоговое окно для сохранения файла с расширением .txt
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        #Если пользователь выбрал путь для сохранения файла
        if file_path:
            #Открываем файл для записи
            with open(file_path, 'w') as file:
                #Проходим по всем клиентам и записываем их данные в файл
                for client in self.company.clients:
                    file.write(f"Клиент: {client.name}, Вес груза: {client.cargo_weight}, VIP статус: {client.vip_status}\n")
                #Проходим по всем транспортным средствам и записываем их данные в файл
                for vehicle in self.company.vehicles:
                    if vehicle.vehicle_type == "Фургон":
                        #Если транспорт - фургон, записываем его тип, грузоподъемность и наличие холодильника
                        file.write(f"Транспорт: {vehicle.vehicle_type}, Грузоподъемность: {vehicle.capacity}, Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}\n")
                    else:
                        #Если транспорт - судно, записываем его тип, грузоподъемность и название судна
                        file.write(f"Транспорт: {vehicle.vehicle_type}, Грузоподъемность: {vehicle.capacity}, Название судна: {vehicle.name}\n")
            #Устанавливаем статус о том, что результаты успешно экспортированы
            self.status.set("Результаты экспортированы.")

    def show_about(self):
        #Показываем информационное сообщение о программе
        messagebox.showinfo("О программе", "Лабораторная работа №12\nВариант: 3\nФИО: Латышев Ярослав Юрьевич")

#Проверяем, является ли данный модуль основным (точкой входа в программу)
if __name__ == "__main__":
    # Создаем основное окно приложения
    root = tk.Tk()
    #Создаем экземпляр класса приложения TransportApp, передавая основное окно
    app = TransportApp(root)
    #Запускаем главный цикл обработки событий Tkinter
    root.mainloop()
