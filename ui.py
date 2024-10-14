from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

class FortressInfoPopup(Popup):
    def __init__(self, kingdom, fortress_coords, **kwargs):
        super(FortressInfoPopup, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.8)

        # Убираем заголовок окна
        self.title = ''  # Устанавливаем пустую строку, чтобы не было "Non title"

        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Заголовок
        title_label = Label(text=f"Информация о городе {fortress_coords}", font_size='24sp', halign='center', size_hint_y=None, height=40)
        title_label.bind(size=title_label.setter('text_size'))  # Для центрирования текста
        main_layout.add_widget(title_label)

        # Создаем верхний контейнер для войск
        troops_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=200)

        # Бокс для атакующих войск
        attacking_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        attacking_box.add_widget(Label(text="Атакующие войска", font_size='20sp'))
        self.attacking_units_list = ScrollView(size_hint=(1, None), size=(self.width, 150))
        self.attacking_units_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.attacking_units_box.bind(minimum_height=self.attacking_units_box.setter('height'))
        attacking_box.add_widget(self.attacking_units_list)
        self.attacking_units_list.add_widget(self.attacking_units_box)
        troops_layout.add_widget(attacking_box)

        # Бокс для защитных войск
        defending_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        defending_box.add_widget(Label(text="Защитные войска", font_size='20sp'))
        self.defending_units_list = ScrollView(size_hint=(1, None), size=(self.width, 150))
        self.defending_units_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.defending_units_box.bind(minimum_height=self.defending_units_box.setter('height'))
        defending_box.add_widget(self.defending_units_list)
        self.defending_units_list.add_widget(self.defending_units_box)
        troops_layout.add_widget(defending_box)

        # Добавляем верхний контейнер в основной макет
        main_layout.add_widget(troops_layout)

        # Бокс для построенных зданий
        buildings_box = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        buildings_box.add_widget(Label(text="Построенные здания", font_size='20sp'))
        self.buildings_list = ScrollView(size_hint=(1, None), size=(self.width, 150))
        self.buildings_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.buildings_box.bind(minimum_height=self.buildings_box.setter('height'))
        self.buildings_list.add_widget(self.buildings_box)
        buildings_box.add_widget(self.buildings_list)

        # Добавляем бокс зданий в основной макет
        main_layout.add_widget(buildings_box)

        # Кнопка для закрытия окна
        close_button = Button(text="Закрыть", size_hint_y=None, height=50)
        close_button.bind(on_press=self.dismiss)
        main_layout.add_widget(close_button)

        # Устанавливаем основной макет для окна
        self.content = main_layout

        # Загружаем данные о войсках и зданиях
        self.load_troops(kingdom, fortress_coords)
        self.load_buildings(kingdom, fortress_coords)



    def load_troops(self, kingdom, fortress_coords):
        # Здесь вы загружаете данные о войсках, например:
        attacking_units = self.get_attacking_units(kingdom, fortress_coords)
        defending_units = self.get_defending_units(kingdom, fortress_coords)

        # Заполняем бокс атакующих войск
        for unit in attacking_units:
            self.attacking_units_box.add_widget(Label(text=unit))

        # Заполняем бокс защитных войск
        for unit in defending_units:
            self.defending_units_box.add_widget(Label(text=unit))

    def load_buildings(self, kingdom, fortress_coords):
        # Здесь вы загружаете данные о зданиях, например:
        buildings = self.get_buildings(kingdom, fortress_coords)

        # Заполняем бокс зданий
        for building in buildings:
            self.buildings_box.add_widget(Label(text=building))

    def get_attacking_units(self, kingdom, fortress_coords):
        # Вернуть список атакующих войск (пример данных)
        return ["Атакующий юнит 1", "Атакующий юнит 2"]

    def get_defending_units(self, kingdom, fortress_coords):
        # Вернуть список защитных войск (пример данных)
        return ["Защитный юнит 1", "Защитный юнит 2"]

    def get_buildings(self, kingdom, fortress_coords):
        # Вернуть список построенных зданий (пример данных)
        return ["Здание 1", "Здание 2"]
