from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Line

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
        self.food = 500
        self.population = 100
        self.hospitals = 0
        self.factories = 0
        self.taxes = 0
        self.tax_set = False  # Флаг, установлен ли налог
        self.custom_tax_rate = None  # Новый атрибут для хранения пользовательской ставки налога
        self.cities_buildings = {city: {'hospitals': 0, 'factories': 0} for city in cities}  # Словарь для хранения зданий в городах
        self.resources = {'Деньги': self.money, 'Свободные люди': self.free_peoples, 'Еда': self.food, 'Население': self.population}
        self.economic_params = {
            # Упрощение параметров для улучшения читаемости
            "Аркадия": {"hospital": {"gain_people": 90, "cost_money": 250}, "factory": {"gain_food": 220, "cost_people": 30}, "food_consumption": 1.8, "tax_rate": 0.09},
            "Селестия": {"hospital": {"gain_people": 70, "cost_money": 220}, "factory": {"gain_food": 240, "cost_people": 35}, "food_consumption": 1.8, "tax_rate": 0.07},
            "Хиперион": {"hospital": {"gain_people": 110, "cost_money": 220}, "factory": {"gain_food": 230, "cost_people": 40}, "food_consumption": 1.7, "tax_rate": 0.07},
            "Этерия": {"hospital": {"gain_people": 140, "cost_money": 200}, "factory": {"gain_food": 200, "cost_people": 50}, "food_consumption": 1.5, "tax_rate": 0.05},
            "Халидон": {"hospital": {"gain_people": 130, "cost_money": 180}, "factory": {"gain_food": 200, "cost_people": 70}, "food_consumption": 1.2, "tax_rate": 0.03},
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
        self.cities_buildings[city]['factories'] += 1  # Увеличиваем счетчик фабрик в выбранном городе

    def build_hospital(self, city):
        """Увеличить количество больниц в определенном городе и обновить ресурсы."""
        self.hospitals += 1
        self.cities_buildings[city]['hospitals'] += 1  # Увеличиваем счетчик больниц в выбранном городе

    def get_city_buildings(self, city):
        """Получение информации о зданиях в указанном городе."""
        return self.cities_buildings.get(city, {})

    def collect_people(self):
        people = self.economic_params[self.faction]["hospital"]["gain_people"]
        people_f = self.economic_params[self.faction]["factory"]["cost_people"]
        self.free_peoples += (self.hospitals * people) - (self.factories * people_f)
        self.population += self.free_peoples

    def collect_food(self):
        food = self.economic_params[self.faction]["factory"]["gain_food"]
        koef = self.economic_params[self.faction]["food_consumption"]
        self.food += (self.factories * food) - (self.population * koef)

    def collect_money(self):
        income = self.calculate_tax_income()
        cost_money = self.economic_params[self.faction]["hospital"]["cost_money"]
        self.money += income - (self.hospitals * cost_money)

    def update_resources(self):
        """Обновление текущих ресурсов, с проверкой на минимальное значение 0."""
        self.collect_people()
        self.collect_food()
        self.collect_money()

        # Проверка, чтобы ресурсы не опускались ниже 0
        self.resources["Деньги"] = max(self.money, 0)
        self.resources["Свободные люди"] = max(self.free_peoples, 0)
        self.resources["Еда"] = max(self.food, 0)
        self.resources["Население"] = max(self.population, 0)

        print(f"Ресурсы обновлены: {self.resources}, Больницы: {self.hospitals}, Фабрики: {self.factories}")

    def get_resources(self):
        """Получение текущих ресурсов"""
        return self.resources

    def end_game(self):
        if self.population == 0:
            return False


# Логика для открытия попапа и строительства
def build_structure(building, city, faction):
    if building != "Здания" and city != "Города":
        # Проверка выбора здания и города
        if building and city:
            if building == 'Больница':
                faction.build_hospital(city)
            elif building == 'Фабрика':
                faction.build_factory(city)

            # Сообщение об успешном строительстве
            Popup(title=f"{building} построена!", content=Label(text=f"{building} построена в городе {city}"),
                  size_hint=(0.5, 0.5)).open()
        else:
            Popup(title="Ошибка", content=Label(text="Не выбрано здание или город!"), size_hint=(0.5, 0.5)).open()
    else:
        Popup(title="Ошибка", content=Label(text="Выберите здание и город!"), size_hint=(0.5, 0.5)).open()


def show_city_statistics(city, faction):
    """Показать статистику зданий в выбранном городе."""
    buildings = faction.get_city_buildings(city)
    content = f"В городе {city}:\nБольницы: {buildings['hospitals']}\nФабрики: {buildings['factories']}"
    Popup(title=f"Статистика для города {city}", content=Label(text=content), size_hint=(0.5, 0.5)).open()


def open_build_popup(faction):
    build_popup = Popup(title="Построить здание", size_hint=(0.8, 0.8))
    main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)
    building_box = BoxLayout(orientation='vertical', size_hint=(0.4, 1))

    building_label = Label(text="Выберите здание:")
    building_box.add_widget(building_label)

    building_dropdown = DropDown()
    for building, icon in BUILDINGS.items():
        btn = Button(text=building, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: building_dropdown.select(btn.text))
        building_dropdown.add_widget(btn)

    building_main_button = Button(text="Здания", size_hint=(1, None), height=44)
    building_main_button.bind(on_release=building_dropdown.open)
    building_dropdown.bind(on_select=lambda instance, x: setattr(building_main_button, 'text', x))

    building_box.add_widget(building_main_button)
    main_layout.add_widget(building_box)

    city_box = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
    city_label = Label(text="Выберите город:")
    city_box.add_widget(city_label)

    city_dropdown = DropDown()
    for city in faction.cities:
        btn = Button(text=city, size_hint_y=None, height=44)
        btn.bind(on_release=lambda btn: city_dropdown.select(btn.text))
        city_dropdown.add_widget(btn)

    city_main_button = Button(text="Города", size_hint=(1, None), height=44)
    city_main_button.bind(on_release=city_dropdown.open)
    city_dropdown.bind(on_select=lambda instance, x: setattr(city_main_button, 'text', x))

    city_box.add_widget(city_main_button)
    main_layout.add_widget(city_box)

    button_box = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
    build_button = Button(text="Построить", size_hint=(1, None), height=44)
    build_button.bind(on_release=lambda x: build_structure(building_main_button.text, city_main_button.text, faction))

    # Кнопка для показа статистики
    stats_button = Button(text="Статистика", size_hint=(1, None), height=44)
    stats_button.bind(on_release=lambda x: show_city_statistics(city_main_button.text, faction))

    button_box.add_widget(build_button)
    button_box.add_widget(stats_button)
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

    build_btn = Button(text="Строительство", size_hint_x=0.33, size_hint_y=None, height=50)
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

