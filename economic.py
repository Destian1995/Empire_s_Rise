from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Line
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import datetime
import os
import re
import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from collections import defaultdict
import matplotlib.pyplot as plt
import io


def clear_building_log():
    """Очищает данные в файле building_changes.log."""
    with open('files/config/buildings_city.log', 'w') as file:
        file.write('')  # Просто открываем файл в режиме записи, что удаляет все его содержимое


# Очищаем файл перед началом программы
clear_building_log()

# Функция для записи изменений в файл
def log_building_change(faction_name, city, building_type, action, amount):
    """Логирует изменения в количестве зданий."""
    with open('files/config/buildings_city.log', 'a') as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Faction: {faction_name}, City: {city}, Action: {action} {amount} {building_type}(s)\n"
        file.write(log_entry)


# Список доступных зданий с иконками
BUILDINGS = {
    'Больница': 'files/buildings/medic.jpg',
    'Фабрика': 'files/buildings/fabric.jpg',
}


class Faction:
    def __init__(self, name, cities):
        self.faction = name
        self.cities = cities
        self.money = 400
        self.free_peoples = 100
        self.food = 600
        self.population = 100
        self.hospitals = 0
        self.factories = 0
        self.taxes = 0
        self.food_info = 0
        self.work_peoples = 0
        self.money_info = 0
        self.born_peoples = 0
        self.money_up = 0
        self.taxes_info = 0
        self.food_peoples = 0
        self.tax_effects = 0
        self.food_price_history = []  # История цен на еду
        self.current_food_price = 0  # Текущая цена на еду
        self.turns = 0  # Счетчик ходов
        self.tax_set = False  # Флаг, установлен ли налог
        self.custom_tax_rate = None  # Новый атрибут для хранения пользовательской ставки налога
        self.cities_buildings = {city: {'hospitals': 0, 'factories': 0} for city in cities}  # Словарь для хранения зданий в городах
        self.resources = {'Кроны': self.money, 'Рабочие': self.free_peoples, 'Еда': self.food, 'Население': self.population}
        self.economic_params = {
            # Упрощение параметров для улучшения читаемости
            "Аркадия": {"tax_rate": 0.03},
            "Селестия": {"tax_rate": 0.015},
            "Хиперион": {"tax_rate": 0.015},
            "Этерия": {"tax_rate": 0.012},
            "Халидон": {"tax_rate": 0.01},
        }

        self.generate_food_price()  # Генерация начальной цены на еду

    def get_income_per_person(self):
        """Получение дохода с одного человека для данной фракции."""
        if self.tax_set and self.custom_tax_rate is not None:
            return self.custom_tax_rate
        params = self.economic_params[self.faction]
        return params["tax_rate"]

    def calculate_tax_income(self):
        """Расчет дохода от налогов с учетом установленной ставки."""
        if not self.tax_set:
            print("Налог не установлен. Прироста от налогов нет.")
            self.taxes = 0
        else:
            # Используем пользовательскую ставку налога или базовую, если пользовательская не задана
            tax_rate = self.custom_tax_rate if self.custom_tax_rate is not None else self.get_base_tax_rate()
            self.taxes = self.population * tax_rate  # Применяем базовую налоговую ставку
        return self.taxes

    def set_taxes(self, new_tax_rate):
        """Установка нового уровня налогов и обновление ресурсов."""
        self.custom_tax_rate = self.get_base_tax_rate() * new_tax_rate   # Применяем процент к базовой ставке
        self.tax_set = True
        self.calculate_tax_income()

    def tax_effect(self, tax_rate):
        if 50 > tax_rate >= 35:
            return -250
        elif 75 > tax_rate >= 50:
            return -8000
        elif 90 > tax_rate >= 75:
            return -22500
        elif tax_rate >= 90:
            return -70000
        elif 15 > tax_rate:
            return 450
        else:
            return 90

    def apply_tax_effect(self, tax_rate):
        # Рассчитать и применить эффект налогов на население
        effect = self.tax_effect(tax_rate)
        self.tax_effects = effect
        return effect


    def calculate_base_tax_rate(self, tax_rate):
        """Формула расчёта базовой налоговой ставки для текущей фракции."""
        params = self.economic_params[self.faction]
        base_tax_rate = params["tax_rate"]  # Базовая ставка налога для текущей фракции

        # Формируем корректировочный коэффициент на основе введённой ставки
        multiplier = tax_rate
        # Возвращаем корректированную налоговую ставку
        return base_tax_rate * multiplier

    def get_base_tax_rate(self):
        """Получение базовой налоговой ставки для текущей фракции."""
        return self.economic_params[self.faction]["tax_rate"]

    def build_factory(self, city):
        """Увеличить количество фабрик в определенном городе и обновить ресурсы."""
        self.factories += 1
        self.cities_buildings[city]['factories'] += 1
        log_building_change(self.faction, city, "factory", "Built", 1)  # Логируем постройку фабрики

    def build_hospital(self, city):
        """Увеличить количество больниц в определенном городе и обновить ресурсы."""
        self.hospitals += 1
        self.cities_buildings[city]['hospitals'] += 1
        log_building_change(self.faction, city, "hospital", "Built", 1)  # Логируем постройку больницы

    def get_city_buildings(self, city):
        """Получение информации о зданиях в указанном городе."""
        return self.cities_buildings.get(city, {})

    def update_buildings(self):
        """Обновляет количество госпиталей и фабрик для текущей фракции по данным из лог-файла."""
        log_file = 'files/config/buildings_city.log'

        # Сброс значений перед обновлением
        self.hospitals = 0
        self.factories = 0

        if os.path.exists(log_file):
            with open(log_file, 'r') as file:
                for line in file:
                    # Проверяем, что строка относится к текущей фракции
                    if f"Faction: {self.faction}" in line:
                        # Извлекаем координаты города
                        match = re.search(r'City: \((\d+), (\d+)\)', line)
                        if match:
                            # Проверяем тип здания
                            if "hospital" in line:
                                self.hospitals += 1
                            elif "factory" in line:
                                self.factories += 1
        else:
            print(f"Log file {log_file} not found!")

        print(
            f"Обновлено количество зданий для {self.faction}: Госпиталей = {self.hospitals}, Фабрик = {self.factories}")

    def cash_build(self, money):
        """Списывает деньги, если их хватает, и возвращает True, иначе False."""
        if self.money >= money:
            self.money -= money
            return True
        else:
            return False

    def update_cash(self):
        self.resources['Кроны'] = self.money
        self.resources['Рабочие'] = self.free_peoples
        self.resources['Еда'] = self.food
        return self.resources

    def update_resources(self):
        """Обновление текущих ресурсов, с проверкой на минимальное значение 0 и округлением до целых чисел."""
        self.update_buildings()

        # Генерация новой цены на еду
        self.generate_food_price()

        # Коэффициенты для каждой фракции
        faction_coefficients = {
            'Аркадия': {'free_peoples_gain': 190, 'free_peoples_loss': 30, 'money_loss': 100, 'food_gain': 600,
                        'food_loss': 1.2},
            'Селестия': {'free_peoples_gain': 170, 'free_peoples_loss': 20, 'money_loss': 200, 'food_gain': 540,
                         'food_loss': 1.1},
            'Хиперион': {'free_peoples_gain': 210, 'free_peoples_loss': 40, 'money_loss': 200, 'food_gain': 530,
                         'food_loss': 0.7},
            'Этерия': {'free_peoples_gain': 240, 'free_peoples_loss': 60, 'money_loss': 200, 'food_gain': 500,
                       'food_loss': 0.5},
            'Халидон': {'free_peoples_gain': 230, 'free_peoples_loss': 50, 'money_loss': 300, 'food_gain': 500,
                        'food_loss': 0.2},
        }

        # Получение коэффициентов для текущей фракции
        faction = self.faction
        if faction not in faction_coefficients:
            raise ValueError(f"Фракция '{faction}' не найдена.")

        coeffs = faction_coefficients[faction]

        # Обновление ресурсов с учетом коэффициентов
        self.free_peoples += int((self.hospitals * 500) - (self.factories * 200)) + self.tax_effects
        self.born_peoples = int(self.hospitals * 500)
        self.work_peoples = int(self.factories * 200)
        self.money += int(self.calculate_tax_income() - (self.hospitals * coeffs['money_loss']))
        self.money_info = int(self.hospitals * coeffs['money_loss'])
        self.money_up = int(self.calculate_tax_income() - (self.hospitals * coeffs['money_loss']))
        self.taxes_info = int(self.calculate_tax_income())

        # Учитываем, что одна фабрика может прокормить 1000 людей
        self.food += int((self.factories * 1000) - (self.population * coeffs['food_loss']))
        self.food_info = int((self.factories * 1000) - (self.population * coeffs['food_loss']))
        self.food_peoples = int(self.population * coeffs['food_loss'])

        # Проверяем, будет ли население увеличиваться
        if self.food > 0:
            self.population += int(self.free_peoples)  # Увеличиваем население только если есть еда
        else:
            # Логика убыли населения при недостатке еды
            if self.population > 100:
                loss = int(self.population * 0.45)  # 45% от населения
                self.population -= loss
            else:
                loss = min(self.population, 50)  # Обнуление по 50, но не ниже 0
                self.population -= loss
            self.free_peoples = 0  # Все рабочие обнуляются, так как еды нет



        # Проверка, чтобы ресурсы не опускались ниже 0
        self.resources.update({
            "Кроны": max(int(self.money), 0),
            "Рабочие": max(int(self.free_peoples), 0),
            "Еда": max(int(self.food), 0),
            "Население": max(int(self.population), 0)
        })

        print(f"Ресурсы обновлены: {self.resources}, Больницы: {self.hospitals}, Фабрики: {self.factories}")


    def get_resources(self):
        """Получение текущих ресурсов"""
        return self.resources

    def end_game(self):
        if self.population == 0:
            return False


    def generate_food_price(self):
        """Генерация случайной цены на еду"""
        self.current_food_price = random.randint(3000, 47000)
        self.food_price_history.append(self.current_food_price)

        # Ограничение длины истории цен до 15 элементов
        if len(self.food_price_history) > 15:
            self.food_price_history.pop(0)

        self.turns += 1

    def trade_food(self, action):
        """Торговля едой"""
        if action == 'buy':  # Преобразование бушелей в еду
            self.money -= self.current_food_price
            self.food += 10000  # Прямое добавление еды
        elif action == 'sell':  # Преобразование бушелей в еду
            self.money += self.current_food_price
            self.food -= 10000  # Прямое уменьшение еды

    def plot_food_price(self):
        """Генерация графика цен на еду"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.food_price_history, marker='o')
        plt.title('История цен на еду за 10000 единиц(бушель)')
        plt.xlabel('Ходы')
        plt.ylabel('Цена за бушель (кроны)')
        plt.grid()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()

# Логика для отображения сообщения об ошибке средств
def show_error_message(message):
    error_popup = Popup(title="Ошибка", content=Label(text=message), size_hint=(0.5, 0.5))
    error_popup.open()

# Логика для успешного строительства
def show_success_message(building, city):
    success_popup = Popup(title="Успешно", content=Label(text=f"Здание '{building}' построено в городе '{city}'!"), size_hint=(0.5, 0.5))
    success_popup.open()

# Функция для постройки здания
def build_structure(building, city, faction):
    if building == "Здания" or city == "Города":
        show_error_message("Выберите здание для постройки и город!")
        return

    if building == "Фабрика":
        if faction.cash_build(100):
            faction.build_factory(city)
            show_success_message(building, city)
        else:
            show_error_message("Недостаточно денег для постройки фабрики! \n  Стоимость фабрики 100 крон")
    elif building == "Больница":
        if faction.cash_build(50):
            faction.build_hospital(city)
            show_success_message(building, city)
        else:
            show_error_message("Недостаточно денег для постройки больницы! \n  Стоимость больницы 50 крон")


# Функция открытия окна постройки зданий
def open_build_popup(faction):
    build_popup = Popup(title="Состояние государства", size_hint=(0.8, 0.8))

    main_layout = FloatLayout()

    # Информационный блок с общими показателями ресурсов
    stats_box = BoxLayout(orientation='vertical', size_hint=(1, 0.65), pos_hint={'x': 0, 'y': 0.25}, padding=[30, 45, 45, 10])

    # Используем TextInput для отображения информации о ресурсах
    stats_info = (
        f"Чистое производство еды фабриками: {faction.food_info} / Потребление рабочих: {faction.work_peoples}\n"
        f"Прирост численности рабочих: {faction.born_peoples} / Потребление денег больницами: {faction.money_info}\n"
        f"Чистый прирост денег: {faction.money_up}\n"
        f"Доход от налогов: {faction.taxes_info}\n"
        f"Потребление еды: {faction.food_peoples}\n"
        f"Количество больниц: {faction.hospitals}\n"
        f"Количество фабрик: {faction.factories}\n"
        f"1 больница дает(за ход): 500 рабочих и требует 100 крон\n"
        f"1 фабрика дает(за ход): может прокормить 1000 населения, но требует 200 рабочих\n"
        f"Эффект от налогов (Изменение рабочих): {faction.apply_tax_effect(int(faction.current_tax_rate[:-1])) if faction.tax_set else 'Налог не установлен'}\n"
    )

    # Увеличиваем высоту текстового блока для отображения новой строки
    stats_text_box = TextInput(text=stats_info, readonly=True, size_hint=(1, None), height=300)
    stats_text_box.background_color = (0.9, 0.9, 0.9, 1)
    stats_box.add_widget(stats_text_box)

    main_layout.add_widget(stats_box)

    # Блок выбора зданий (опускаем вниз)
    building_box = BoxLayout(orientation='vertical', size_hint=(0.3, 0.2), pos_hint={'x': 0.05, 'y': 0.05})  # Выровнено по нижнему краю
    building_main_button = Button(text="Здания", size_hint=(1, None), height=44)
    building_dropdown = DropDown(auto_dismiss=False)
    for building, icon in BUILDINGS.items():
        btn = Button(text=building, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: building_dropdown.select(btn.text))
        building_dropdown.add_widget(btn)
    building_main_button.bind(on_release=building_dropdown.open)
    building_dropdown.bind(on_select=lambda instance, x: setattr(building_main_button, 'text', x))

    building_box.add_widget(Label(text="Выберите здание:", size_hint=(1, None), height=30))
    building_box.add_widget(building_main_button)

    main_layout.add_widget(building_box)

    # Блок выбора города (опускаем вниз)
    city_box = BoxLayout(orientation='vertical', size_hint=(0.3, 0.2), pos_hint={'x': 0.35, 'y': 0.05})  # Выровнено по нижнему краю
    city_main_button = Button(text="Города", size_hint=(1, None), height=44)
    city_dropdown = DropDown(auto_dismiss=False)
    for city in faction.cities:
        btn = Button(text=city, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: city_dropdown.select(btn.text))
        city_dropdown.add_widget(btn)
    city_main_button.bind(on_release=city_dropdown.open)
    city_dropdown.bind(on_select=lambda instance, x: setattr(city_main_button, 'text', x))

    city_box.add_widget(Label(text="Выберите город:", size_hint=(1, None), height=30))
    city_box.add_widget(city_main_button)

    main_layout.add_widget(city_box)

    # Блок кнопки для постройки зданий (опускаем вниз и выравниваем с другими блоками)
    button_box = BoxLayout(orientation='vertical', size_hint=(0.3, 0.2), pos_hint={'x': 0.7, 'y': 0.05})  # Выровнено по нижнему краю
    build_button = Button(text="Построить", size_hint=(1, None), height=44)
    build_button.bind(on_release=lambda x: build_structure(building_main_button.text, city_main_button.text, faction))

    button_box.add_widget(build_button)
    main_layout.add_widget(button_box)

    build_popup.content = main_layout
    build_popup.open()


#---------------------------------------------------------------

# Функция для открытия окна торговли
def open_trade_popup(game_instance):
    """Открытие окна торговли с графиком цен"""
    game_instance.generate_food_price()  # Генерация новой цены на еду при открытии окна

    trade_layout = BoxLayout(orientation='vertical', padding=10)

    # Генерация и сохранение графика как изображения
    plot_data = game_instance.plot_food_price()
    with open('food_price.png', 'wb') as f:
        f.write(plot_data)  # Сохранение изображения

    img = Image(source='food_price.png', size_hint_y=None, height=400)

    # Кнопки для покупки и продажи
    button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
    buy_btn = Button(text="Купить 10000 еды", size_hint_x=0.5)
    sell_btn = Button(text="Продать 10000 еды", size_hint_x=0.5)
    button_layout.add_widget(buy_btn)
    button_layout.add_widget(sell_btn)

    trade_layout.add_widget(img)  # Добавляем изображение графика в основной контейнер
    trade_layout.add_widget(button_layout)  # Добавляем кнопки в основной контейнер

    trade_popup = Popup(title="Торговля", content=trade_layout, size_hint=(0.8, 0.8))

    buy_btn.bind(on_press=lambda x: game_instance.trade_food('buy'))
    sell_btn.bind(on_press=lambda x: game_instance.trade_food('sell'))

    trade_popup.open()

    # Обновление графика при закрытии попапа
    trade_popup.bind(on_dismiss=lambda instance: update_food_price_graph(game_instance, img))

def update_food_price_graph(game_instance, img):
    """Обновление графика цен на еду"""
    plot_data = game_instance.plot_food_price()  # Генерируем новое изображение графика
    with open('food_price.png', 'wb') as f:
        f.write(plot_data)  # Сохраняем изображение
    img.source = 'food_price.png'  # Обновляем источник изображения
    img.reload()  # Перезагружаем изображение для обновления отображения


def open_tax_popup(faction):
    """Открытие попапа для выбора ставки налога через выпадающий список"""

    tax_popup = Popup(title="Управление налогами", size_hint=(0.8, 0.4))

    main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    # Устанавливаем начальное значение для налоговой ставки
    current_tax_rate = '0%' if not faction.tax_set else f"{faction.current_tax_rate}"  # Значение по умолчанию, если налог не установлен

    # Создание выпадающего списка для выбора налоговой ставки
    tax_spinner = Spinner(
        text=current_tax_rate,  # Устанавливаем текущее значение
        values=('0%', '5%', '15%', '25%', '35%', '50%', '65%', '75%', '85%', '95%', '100%')  # Добавляем '0%'
    )

    # Метка для текущей ставки налога
    tax_label = Label(text=f"Текущая ставка налога: {tax_spinner.text}")

    def update_tax_rate(spinner, text):
        """Функция для обновления ставки налога при выборе из списка"""
        tax_label.text = f"Текущая ставка налога: {text}"  # Обновляем текст метки при выборе
        tax_rate = int(text[:-1])  # Убираем '%' и приводим к числу
        faction.set_taxes(tax_rate) # Устанавливаем ставку налога
        faction.apply_tax_effect(tax_rate) # Считаем отрицательный эффект

    tax_spinner.bind(text=update_tax_rate)

    # Кнопка для подтверждения нового налога
    set_tax_button = Button(text="Установить уровень налогов", size_hint_y=None, height=44)

    def set_tax(instance):
        """Установить новый уровень налогов и закрыть попап"""
        faction.current_tax_rate = tax_spinner.text  # Обновляем текущее значение налога в faction
        tax_popup.dismiss()

    set_tax_button.bind(on_press=set_tax)

    # Добавляем элементы в layout
    main_layout.add_widget(tax_label)
    main_layout.add_widget(tax_spinner)
    main_layout.add_widget(set_tax_button)

    tax_popup.content = main_layout
    tax_popup.open()


def start_economy_mode(faction, game_area):
    """Инициализация экономического режима для выбранной фракции"""

    # Кнопки для управления экономикой
    economy_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    build_btn = Button(text="Состояние государства", size_hint_x=0.33, size_hint_y=None, height=50)
    trade_btn = Button(text="Торговля", size_hint_x=0.33, size_hint_y=None, height=50)
    tax_btn = Button(text="Управление налогами", size_hint_x=0.33, size_hint_y=None, height=50)

    economy_layout.add_widget(build_btn)
    economy_layout.add_widget(trade_btn)
    economy_layout.add_widget(tax_btn)

    # Добавляем layout с кнопками в нижнюю часть экрана
    game_area.add_widget(economy_layout)

    # Привязываем кнопку "Построить здание" к функции открытия попапа
    build_btn.bind(on_press=lambda x: open_build_popup(faction))
    tax_btn.bind(on_press=lambda x: open_tax_popup(faction))
    trade_btn.bind(on_press=lambda x: open_trade_popup(faction))

