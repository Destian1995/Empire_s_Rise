from kivy.graphics import Color, Ellipse, Rectangle
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.textinput import TextInput


# Размеры окна
screen_width, screen_height = 1200, 800

# Цвета крепостей
fortress_colors = {
    "Аркадия": (0, 0, 0.5),
    "Селестия": (0, 0.5, 0),
    "Хиперион": (0.5, 0, 0.5),
    "Халидон": (0.5, 0.25, 0),
    "Этерия": (0, 0.5, 0.5)
}

# Координаты крепостей и деревень для каждого княжества
kingdom_points = {
    "Аркадия": {
        "fortresses": [(80, 460), (100, 630), (400, 500), (370, 600)],
        "towns": [(120, 770), (210, 520), (70, 560), (350, 700)]
    },
    "Селестия": {
        "fortresses": [(130, 400), (260, 140), (100, 250)],
        "towns": [(90, 100), (30, 180), (100, 230), (120, 350), (130, 320), (250, 160), (270, 200)]
    },
    "Хиперион": {
        "fortresses": [(410, 120), (410, 320), (510, 200), (310, 170), (520, 620), (750, 540), (660, 380), (890, 520), (750, 150)],
        "towns": [(220, 240), (640, 180), (560, 300), (580, 660), (600, 400), (700, 500), (800, 300), (750, 240)]
    },
    "Халидон": {
        "fortresses": [(820, 160), (940, 280), (1020, 100)],
        "towns": [(980, 570), (950, 420), (870, 260), (890, 300)]
    },
    "Этерия": {
        "fortresses": [(960, 370), (1090, 660), (1120, 310)],
        "towns": [(1000, 400), (1120, 410), (1080, 550)]
    }
}

# Владелец каждой крепости и города
territory_owners = {
    "Аркадия": {
        "fortresses": ["Аркадия"] * len(kingdom_points["Аркадия"]["fortresses"]),
        "towns": ["Аркадия"] * len(kingdom_points["Аркадия"]["towns"])
    },
    "Селестия": {
        "fortresses": ["Селестия"] * len(kingdom_points["Селестия"]["fortresses"]),
        "towns": ["Селестия"] * len(kingdom_points["Селестия"]["towns"])
    },
    "Хиперион": {
        "fortresses": ["Хиперион"] * len(kingdom_points["Хиперион"]["fortresses"]),
        "towns": ["Хиперион"] * len(kingdom_points["Хиперион"]["towns"])
    },
    "Халидон": {
        "fortresses": ["Халидон"] * len(kingdom_points["Халидон"]["fortresses"]),
        "towns": ["Халидон"] * len(kingdom_points["Халидон"]["towns"])
    },
    "Этерия": {
        "fortresses": ["Этерия"] * len(kingdom_points["Этерия"]["fortresses"]),
        "towns": ["Этерия"] * len(kingdom_points["Этерия"]["towns"])
    }
}
class HallOfFameWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(HallOfFameWidget, self).__init__(**kwargs)
        self.add_widget(Image(source='files/menu.jpg', allow_stretch=True, keep_ratio=False))  # Фон зала славы

        # Заголовок
        title = Label(text="[b][color=000000]Зал славы[/color][/b]", font_size='40sp', markup=True,
                      size_hint=(1, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.add_widget(title)

        # Поле для вывода лучших результатов
        self.results_label = Label(text=self.get_top_scores(), font_size='30sp', markup=True, halign="center",
                                   size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5}, color=(0, 0, 0, 5))
        self.add_widget(self.results_label)

        # Кнопка "Назад"
        btn_back = Button(text="Назад", size_hint=(0.3, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1},
                          background_normal='', background_color=(0, 0, 0, 1))
        btn_back.bind(on_press=self.go_back)
        self.add_widget(btn_back)

    def get_top_scores(self):
        # Заглушка для топ-10 лучших результатов, можно заменить на реальную логику
        top_scores = [
            "1. Игрок1 - 9999 очков",
            "2. Игрок2 - 9500 очков",
            "3. Игрок3 - 9200 очков",
            "4. Игрок4 - 9000 очков",
            "5. Игрок5 - 8900 очков",
            "6. Игрок6 - 8700 очков",
            "7. Игрок7 - 8500 очков",
            "8. Игрок8 - 8300 очков",
            "9. Игрок9 - 8000 очков",
            "10. Игрок10 - 7800 очков",
        ]
        return "\n".join(top_scores)

    def go_back(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(MenuWidget())

# Виджет карты
class MapWidget(Widget):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_pos = [0, 0]  # Позиция карты
        self.touch_start = None  # Стартовая позиция касания

        with self.canvas:
            # Отрисовка карты
            self.map_image = Rectangle(source='files/map/map.png', pos=self.map_pos, size=(screen_width, screen_height))
            self.draw_map()

    def draw_map(self):
        for kingdom, points in kingdom_points.items():
            # Отрисовка крепостей
            for i, fortress in enumerate(points["fortresses"]):
                owner = territory_owners[kingdom]["fortresses"][i]
                Color(*fortress_colors[owner])  # Используем цвет владельца
                Ellipse(pos=(fortress[0] + self.map_pos[0], fortress[1] + self.map_pos[1]), size=(20, 20))

            # Отрисовка деревень
            for i, town in enumerate(points["towns"]):
                owner = territory_owners[kingdom]["towns"][i]
                Color(1, 1, 1) if owner == kingdom else Color(*fortress_colors[owner])
                Ellipse(pos=(town[0] + self.map_pos[0], town[1] + self.map_pos[1]), size=(10, 10))

    def on_touch_down(self, touch):
        # Запоминаем начальную точку касания
        self.touch_start = touch.pos

    def on_touch_move(self, touch):
        # Вычисляем смещение
        if self.touch_start:
            dx = touch.x - self.touch_start[0]
            dy = touch.y - self.touch_start[1]
            self.touch_start = touch.pos  # Обновляем точку касания

            # Обновляем позицию карты
            self.map_pos[0] += dx
            self.map_pos[1] += dy
            self.update_map_position()

    def update_map_position(self):
        # Обновляем позицию изображения карты
        self.map_image.pos = self.map_pos

        # Перерисовываем крепости и деревни с новой позицией
        self.canvas.clear()
        with self.canvas:
            Rectangle(source='files/map/map.png', pos=self.map_pos, size=(screen_width, screen_height))
            self.draw_map()

    def capture_territory(self, kingdom, territory_type, index, new_owner):
        """Функция для захвата города или крепости"""
        if territory_type == "fortresses":
            territory_owners[kingdom]["fortresses"][index] = new_owner
        elif territory_type == "towns":
            territory_owners[kingdom]["towns"][index] = new_owner

        # Обновляем карту
        self.update_map_position()

# Меню
class MenuWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(MenuWidget, self).__init__(**kwargs)
        self.add_widget(Image(source='files/menu.jpg', allow_stretch=True, keep_ratio=False))  # Фон меню

        # Заголовок
        title = Label(text="[b][color=000000]Расцвет Империи[/color][/b]", font_size='40sp', markup=True,
                      size_hint=(1, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.9})
        self.add_widget(title)

        # Кнопки
        btn_start_game = Button(text="Старт новой игры", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                background_normal='', background_color=(0, 0, 0, 1))
        btn_start_game.bind(on_press=self.start_game)

        btn_load_game = Button(text="Загрузка ранее сохраненной", size_hint=(0.5, 0.1),
                               pos_hint={'center_x': 0.5, 'center_y': 0.5}, background_normal='', background_color=(0, 0, 0, 1))
        btn_load_game.bind(on_press=self.load_game)

        btn_hall_of_fame = Button(text="Зал славы", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.3},
                                  background_normal='', background_color=(0, 0, 0, 1))
        btn_hall_of_fame.bind(on_press=self.show_hall_of_fame)

        btn_exit = Button(text="Выход", size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.1},
                          background_normal='', background_color=(0, 0, 0, 1))
        btn_exit.bind(on_press=self.exit_game)

        self.add_widget(btn_start_game)
        self.add_widget(btn_load_game)
        self.add_widget(btn_hall_of_fame)
        self.add_widget(btn_exit)

    def start_game(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(KingdomSelectionWidget())

    def load_game(self, instance):
        print("Загрузка игры...")

    def show_hall_of_fame(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(HallOfFameWidget())

    def exit_game(self, instance):
        App.get_running_app().stop()

# Виджет выбора княжества
class KingdomSelectionWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(KingdomSelectionWidget, self).__init__(**kwargs)
        self.add_widget(Image(source='files/menu.jpg', allow_stretch=True, keep_ratio=False))  # Фон выбора княжества

        # Заголовок с черным цветом текста
        self.kingdom_label = Label(text="Выберите княжество", font_size='30sp', size_hint=(1, 0.2),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.85}, color=(0, 0, 0, 1))  # Черный текст
        self.add_widget(self.kingdom_label)

        # Сдвигаем кнопки немного левее
        self.kingdom_buttons = BoxLayout(orientation='vertical', spacing=10, size_hint=(0.4, 0.5),
                                         pos_hint={'center_x': 0.4, 'center_y': 0.5})

        for kingdom in kingdom_points.keys():
            btn = Button(text=kingdom, size_hint=(1, None), height=40)
            btn.bind(on_press=self.select_kingdom)
            self.kingdom_buttons.add_widget(btn)

        self.add_widget(self.kingdom_buttons)

        # Изображение советника
        self.advisor_image = Image(source='files/null.png', size_hint=(0.3, 0.3),
                                   pos_hint={'center_x': 0.8, 'center_y': 0.6})  # Изменение позиции изображения
        self.add_widget(self.advisor_image)

        # Описание княжества в текстовом боксе ниже изображений советников
        self.kingdom_info_box = TextInput(text="", size_hint=(0.35, None), height=120,
                                          pos_hint={'center_x': 0.8, 'center_y': 0.35},  # Понижаем позицию
                                          background_color=(0, 0, 0, 1),
                                          foreground_color=(1, 1, 1, 1),  # Белый текст на черном фоне
                                          readonly=True,  # Отключение редактирования
                                          multiline=True)  # Многострочный текст
        self.add_widget(self.kingdom_info_box)

        self.start_game_button = Button(text="Начать игру", size_hint=(0.4, None), height=70,
                                        pos_hint={'center_x': 0.8, 'center_y': 0.15})
        self.start_game_button.bind(on_press=self.start_game)
        self.add_widget(self.start_game_button)

    def select_kingdom(self, instance):
        selected_kingdom = instance.text
        self.kingdom_info_box.text = self.get_kingdom_info(selected_kingdom)

        # Правильное сопоставление названий княжеств и файлов изображений
        kingdom_map = {
            "Аркадия": "arkadia",
            "Селестия": "celestia",
            "Этерия": "eteria",
            "Хиперион": "giperion",
            "Халидон": "halidon"
        }

        advisor_image_filename = kingdom_map.get(selected_kingdom, "").lower()
        if advisor_image_filename:
            self.advisor_image.source = f'files/sov/sov_{advisor_image_filename}.jpg'
            self.advisor_image.reload()

    def get_kingdom_info(self, kingdom):
        info = {
            "Аркадия": "Аркадия - северное княжество.\n"
                       "Экономика: 8\n"
                       "Армия: 8\n"
                       "Дипломатия: 5\n",
            "Селестия": "Селестия - юго-западное княжество. \n"
                        "Экономика: 7\n"
                        "Армия: 7\n"
                        "Диломатия: 7\n",
            "Хиперион": "Хиперион - западная империя. \n"
                        'Экономика: 8\n'
                        'Армия: 10\n'
                        'Дипломатия: 3\n',
            "Халидон": "Халидон - юго-восточное княжество\n"
                        'Экономика: 6\n'
                        'Армия: 5\n'
                        'Дипломатия: 10\n',
            "Этерия": "Этерия - восточное княжество\n"
                        'Экономика: 6\n'
                        'Армия: 6\n'
                        'Дипломатия: 9\n'
        }
        return info.get(kingdom, "")

    def start_game(self, instance):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(MapWidget())



# Основное приложение
class EmpireApp(App):
    def build(self):
        return MenuWidget()

# Запуск приложения
if __name__ == '__main__':
    EmpireApp().run()
