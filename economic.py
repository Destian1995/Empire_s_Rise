from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.graphics import Color, Line
from resources import ResourceManager
# Список доступных зданий с иконками
BUILDINGS = {
    'Больница': 'files/buildings/medic.jpg',
    'Фабрика': 'files/buildings/fabric.jpg',
}

class Faction:
    def __init__(self, name):
        self.name = name  # Название фракции
        self.population = 0  # Начальное население
        self.taxes = 0           # Начальный уровень налогов
        self.hospitals = 0       # Количество больниц
        self.factories = 0       # Количество мануфактур
        self.food_supply = 0     # Запасы еды
        # Инициализация ResourceManager с названием фракции
        self.resource_manager = ResourceManager(self.name)

        # Получение дохода с одного человека
        self.income_per_person = self.resource_manager.get_income_per_person()  # Получение дохода с одного человека


    def calculate_growth(self):
        """Расчет прироста населения на основе налогов и зданий."""
        growth_rate = 0

        # Налоги
        if self.taxes < 10:
            growth_rate += 5  # Высокая скорость прироста
        elif self.taxes < 30:
            growth_rate += 2  # Средняя скорость прироста
        elif self.taxes < 50:
            growth_rate = 0    # Нет эффекта
        elif self.taxes < 70:
            growth_rate -= 2   # Небольшой отток населения
        elif self.taxes < 80:
            growth_rate -= 5   # Высокий отток населения
        elif self.taxes <= 100:
            growth_rate = -10   # Восстания и другие проблемы

        # Учитываем прирост от больниц
        growth_rate += self.hospitals // 2  # Каждая 2-я больница дает прирост

        # Учитываем запасы еды от мануфактур
        if self.food_supply > 0:
            growth_rate += self.factories // 3  # Каждая 3-я мануфактура дает прирост

        return growth_rate

    def update_population(self):
        """Обновление населения на основе прироста."""
        growth = self.calculate_growth()
        self.population += growth
        if self.population < 0:
            self.population = 0  # Не допускаем отрицательного населения

    def set_taxes(self, new_tax_rate):
        """Установка нового уровня налогов и обновление населения."""
        self.taxes = new_tax_rate
        self.update_population()

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

def open_tax_popup(faction):
    """Открытие попапа для управления налогами"""

    # Создаем попап для налогов
    tax_popup = Popup(title="Управление налогами", size_hint=(0.8, 0.8))

    # Основной контейнер
    main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

    # Метка для отображения текущего уровня налогов
    tax_label = Label(text=f"Уровень налогов: {faction.taxes}%", size_hint_y=None, height=44)
    main_layout.add_widget(tax_label)

    # Метка для отображения дохода с одного человека
    income_label = Label(text=f"Доход с одного человека: {faction.income_per_person}", size_hint_y=None, height=44)
    main_layout.add_widget(income_label)

    # Слайдер для установки уровня налогов
    tax_slider = Slider(min=0, max=100, value=faction.taxes)
    main_layout.add_widget(tax_slider)

    # Функция обновления меток при изменении значения слайдера
    def update_tax_label(instance, value):
        faction.set_taxes(value)  # Устанавливаем новые налоги
        tax_label.text = f"Уровень налогов: {int(value)}%"
        income_label.text = f"Доход с одного человека: {faction.income_per_person:.2f}"  # Обновляем доход с одного гражданина


    # Привязываем обновление меток к слайдеру
    tax_slider.bind(value=update_tax_label)

    # Кнопка для закрытия попапа
    close_button = Button(text="Закрыть", size_hint_y=None, height=50)
    close_button.bind(on_press=tax_popup.dismiss)
    main_layout.add_widget(close_button)

    tax_popup.content = main_layout
    tax_popup.open()


def set_taxes(faction, new_tax_rate, popup):
    """Установка налогов и обновление населения"""
    faction.set_taxes(new_tax_rate)

    # Передаем обновленную ставку в ResourceManager
    resource_manager = ResourceManager(faction.name)
    resource_manager.economic_params[faction.name]["tax_rate"] = new_tax_rate

    # Закрываем попап после установки налогов
    popup.dismiss()

    # Отображаем текущее население
    population_popup = Popup(title="Население обновлено",
                             content=Label(text=f"Текущее население: {faction.population}"),
                             size_hint=(0.6, 0.6))
    population_popup.open()


def open_build_popup(faction):
    """Открытие попапа для строительства здания"""

    # Создаем попап для строительства здания
    build_popup = Popup(title="Построить здание", size_hint=(0.8, 0.8))

    # Основной контейнер
    main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

    # Бокс для списка зданий (с иконками)
    building_box = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

    label_buildings = Label(text="Выберите здание:", size_hint_y=None, height=44)
    building_box.add_widget(label_buildings)

    # Используем GridLayout для отображения иконок зданий в сетке
    buildings_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
    buildings_grid.bind(minimum_height=buildings_grid.setter('height'))

    # Добавляем ScrollView, чтобы иконки зданий можно было прокручивать
    scroll_view = ScrollView(size_hint=(1, 1))
    scroll_view.add_widget(buildings_grid)

    # Переменная для хранения выбранного здания
    selected_building = {'name': None}

    # Добавляем иконки зданий в сетку
    for building_name, icon_path in BUILDINGS.items():
        btn = Button(size_hint=(None, None), size=(100, 100))
        btn.background_normal = icon_path

        def on_building_select(button, name=building_name):
            # Убираем рамку со всех кнопок
            for widget in buildings_grid.children:
                widget.canvas.after.clear()

            # Добавляем синюю рамку вокруг выбранной кнопки
            with button.canvas.after:
                Color(0, 0, 1, 1)  # Синяя рамка
                Line(rectangle=(button.x, button.y, button.width, button.height), width=2)

            # Устанавливаем выбранное здание
            selected_building['name'] = name

        # Привязываем функцию выбора здания к кнопке
        btn.bind(on_press=on_building_select)

        buildings_grid.add_widget(btn)

    # Добавляем прокручиваемую область зданий
    building_box.add_widget(scroll_view)

    # Бокс для выбора города
    city_box = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

    label_city = Label(text="Выберите город:", size_hint_y=None, height=44)
    city_box.add_widget(label_city)

    # Список городов
    city_list = ['Город 1', 'Город 2', 'Город 3']  # Здесь будет ваш список городов
    city_dropdown = DropDown()
    for city in city_list:
        btn = Button(text=city, size_hint_y=None, height=44)
        btn.bind(on_release=lambda b: city_dropdown.select(b.text))
        city_dropdown.add_widget(btn)

    city_button = Button(text='Выберите город', size_hint_y=None, height=44)
    city_button.bind(on_release=city_dropdown.open)
    city_dropdown.bind(on_select=lambda instance, x: setattr(city_button, 'text', x))

    city_box.add_widget(city_button)

    # Кнопка для строительства
    build_action_button = Button(text="Построить", size_hint_y=None, height=50)
    build_action_button.bind(on_press=lambda x: build_structure(selected_building['name'], city_button.text))

    city_box.add_widget(build_action_button)

    # Добавляем оба бокса в основной макет
    main_layout.add_widget(building_box)
    main_layout.add_widget(city_box)

    build_popup.content = main_layout
    build_popup.open()

def build_structure(building, city):
    """Логика для строительства здания"""
    if building and city:
        print(f"Строим {building} в городе {city}")

        # Закрываем попап после постройки
        popup = Popup(title="Строительство", content=Label(text=f"Строительство {building} в городе {city} завершено."),
                      size_hint=(0.6, 0.6))
        popup.open()
    else:
        error_popup = Popup(title="Ошибка", content=Label(text="Выберите здание и город перед строительством."),
                            size_hint=(0.6, 0.6))
        error_popup.open()