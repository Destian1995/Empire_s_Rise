from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line

# Список доступных зданий с иконками
BUILDINGS = {
    'Больница': 'files/buildings/medic.jpg',
    'Фабрика': 'files/buildings/fabric.jpg',
    'Рынок': 'files/buildings/market.jpg',
    'НИИ': 'files/buildings/nii.jpg',
}


def start_economy_mode(faction, game_area):
    """Инициализация экономического режима для выбранной фракции"""

    # Кнопки для управления экономикой
    economy_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    build_btn = Button(text="Строительство", size_hint_x=0.33, size_hint_y=None, height=50)
    trade_btn = Button(text="Торговля", size_hint_x=0.33, size_hint_y=None, height=50)
    expand_btn = Button(text="Налоги", size_hint_x=0.33, size_hint_y=None, height=50)

    economy_layout.add_widget(build_btn)
    economy_layout.add_widget(trade_btn)
    economy_layout.add_widget(expand_btn)

    # Добавляем layout с кнопками в нижнюю часть экрана
    game_area.add_widget(economy_layout)

    # Привязываем кнопку "Построить здание" к функции открытия попапа
    build_btn.bind(on_press=lambda x: open_build_popup(faction))

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
