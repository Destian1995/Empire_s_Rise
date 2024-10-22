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
from kivy.uix.widget import Widget
import datetime


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

    def cash_resources(self, money, free_peoples):
        if self.money >= money and self.free_peoples >= free_peoples:
            self.money -= money
            self.free_peoples -= free_peoples
            return True
        return False

    def update_resources(self):
        """Обновление текущих ресурсов, с проверкой на минимальное значение 0."""

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
        self.free_peoples += (self.hospitals * 500) - (self.factories * 200)
        self.born_peoples = self.hospitals * 500
        self.work_peoples = self.factories * 200
        self.money += self.calculate_tax_income() - (self.hospitals * coeffs['money_loss'])
        self.money_info = self.hospitals * coeffs['money_loss']
        self.money_up = self.calculate_tax_income() - (self.hospitals * coeffs['money_loss'])
        self.taxes_info = self.calculate_tax_income()

        # Учитываем, что одна фабрика может прокормить 1000 людей
        self.food += (self.factories * 1000) - (self.population * coeffs['food_loss'])
        self.food_info = (self.factories * 1000) - (self.population * coeffs['food_loss'])
        self.food_peoples = (self.population * coeffs['food_loss'])

        # Проверяем, будет ли население увеличиваться
        if self.food > 0:
            self.population += self.free_peoples  # Увеличиваем население только если есть еда
        else:
            # Логика убыли населения при недостатке еды
            if self.population > 100:
                loss = int(self.population * 0.45)  # 45% от населения
                self.population -= loss
            else:
                loss = min(self.population, 50)  # Обнуление по 25, но не ниже 0
                self.population -= loss
            self.free_peoples = 0  # Все рабочие обнуляются, так как еды нет

        # Проверка, чтобы ресурсы не опускались ниже 0
        self.resources.update({
            "Кроны": max(self.money, 0),
            "Рабочие": max(self.free_peoples, 0),
            "Еда": max(self.food, 0),
            "Население": max(self.population, 0)
        })

        print(f"Ресурсы обновлены: {self.resources}, Больницы: {self.hospitals}, Фабрики: {self.factories}")

    def get_resources(self):
        """Получение текущих ресурсов"""
        return self.resources

    def end_game(self):
        if self.population == 0:
            return False


# Логика для открытия попапа и строительства
# Функция для отображения ошибки
def show_error_message(message):
    error_popup = Popup(title="Ошибка", content=Label(text=message), size_hint=(0.5, 0.5))
    error_popup.open()

# Функция для отображения уведомления об успешной постройке
def show_success_message(building, city):
    success_popup = Popup(title="Успешно", content=Label(text=f"Здание '{building}' построено в городе '{city}'!"), size_hint=(0.5, 0.5))
    success_popup.open()

# Функция для постройки здания
def build_structure(building, city, faction):
    if building == "Здания" or city == "Города":
        show_error_message("Выберите здание для постройки и город!")
        return

    if building == "Фабрика":
        faction.build_factory(city)
    elif building == "Больница":
        faction.build_hospital(city)

    show_success_message(building, city)

# Функция открытия окна постройки зданий
def open_build_popup(faction):
    build_popup = Popup(title="Построить здание", size_hint=(0.8, 0.8))

    main_layout = FloatLayout()

    # Информационный блок с общими показателями ресурсов
    stats_box = BoxLayout(orientation='vertical', size_hint=(0.4, 0.5), pos_hint={'x': 0.05, 'y': 0.1})

    food_label = Label(text=f"Чистое производство еды фабриками: {faction.food_info} / Потребление рабочих: {faction.work_peoples}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})
    income_label = Label(text=f"Прирост численности рабочих: {faction.born_peoples} / Потребление денег больницами: {faction.money_info}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})
    money_label = Label(text=f"Чистый прирост денег: {faction.money_up}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})
    taxes_label = Label(text=f"Доход от налогов: {faction.taxes_info}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})
    food_peoples_label = Label(text=f"Потребление еды: {faction.food_peoples}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})
    hospitals_label = Label(text=f"Количество больниц: {faction.hospitals}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})
    factories_label = Label(text=f"Количество фабрик: {faction.factories}", size_hint=(1, None), height=30, pos_hint={'x': 0.45})

    stats_box.add_widget(food_label)
    stats_box.add_widget(income_label)
    stats_box.add_widget(hospitals_label)
    stats_box.add_widget(factories_label)
    stats_box.add_widget(money_label)
    stats_box.add_widget(taxes_label)
    stats_box.add_widget(food_peoples_label)

    main_layout.add_widget(stats_box)

    # Блок выбора зданий
    building_box = BoxLayout(orientation='vertical', size_hint=(0.3, 0.3), pos_hint={'x': 0.05, 'y': 0.6})
    building_main_button = Button(text="Здания", size_hint=(1, None), height=44)
    building_dropdown = DropDown()
    for building, icon in BUILDINGS.items():
        btn = Button(text=building, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: building_dropdown.select(btn.text))
        building_dropdown.add_widget(btn)
    building_main_button.bind(on_release=building_dropdown.open)
    building_dropdown.bind(on_select=lambda instance, x: setattr(building_main_button, 'text', x))

    building_box.add_widget(Label(text="Выберите здание:", size_hint=(1, None), height=30))
    building_box.add_widget(building_main_button)

    main_layout.add_widget(building_box)

    # Блок выбора города
    city_box = BoxLayout(orientation='vertical', size_hint=(0.3, 0.3), pos_hint={'x': 0.35, 'y': 0.6})
    city_main_button = Button(text="Города", size_hint=(1, None), height=44)
    city_dropdown = DropDown()
    for city in faction.cities:
        btn = Button(text=city, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: city_dropdown.select(btn.text))
        city_dropdown.add_widget(btn)
    city_main_button.bind(on_release=city_dropdown.open)
    city_dropdown.bind(on_select=lambda instance, x: setattr(city_main_button, 'text', x))

    city_box.add_widget(Label(text="Выберите город:", size_hint=(1, None), height=30))
    city_box.add_widget(city_main_button)

    main_layout.add_widget(city_box)

    # Блок кнопки для постройки зданий
    button_box = BoxLayout(orientation='vertical', size_hint=(0.2, 0.5), pos_hint={'x': 0.7, 'y': 0.6})
    build_button = Button(text="Построить", size_hint=(1, None), height=44)
    build_button.bind(on_release=lambda x: build_structure(building_main_button.text, city_main_button.text, faction))

    button_box.add_widget(build_button)
    main_layout.add_widget(button_box)

    build_popup.content = main_layout
    build_popup.open()

#---------------------------------------------------------------

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
        faction.set_taxes(tax_rate)  # Устанавливаем ставку налога

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

    # Привязываем кнопку "Управление налогами"
    tax_btn.bind(on_press=lambda x: open_tax_popup(faction))
