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
from game_process import GameScreen
from ui import *

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

class MapWidget(Widget):
    def __init__(self, selected_kingdom=None, player_kingdom=None, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        self.map_pos = [0, 0]  # Позиция карты
        self.touch_start = None  # Стартовая позиция касания
        self.fortress_rectangles = []  # Список для хранения прямоугольников крепостей
        self.current_player_kingdom = player_kingdom  # Текущее королевство игрока

        # Отрисовка карты
        with self.canvas:
            self.map_image = Rectangle(source='files/map/map.png', pos=self.map_pos, size=(screen_width, screen_height))

        # Отрисовка крепостей
        self.draw_fortresses()


    def set_player_kingdom(self, kingdom_name):
        """Метод для установки и запоминания выбранной фракции."""
        self.selected_kingdom = kingdom_name
        self.current_player_kingdom = kingdom_name  # Устанавливаем текущее королевство игрока
        print(f"Игрок выбрал фракцию: {self.selected_kingdom}")  # Для отладки

    def draw_fortresses(self):
        # Очищаем список прямоугольников крепостей перед новой отрисовкой
        self.fortress_rectangles.clear()

        with self.canvas:
            for kingdom, points in kingdom_points.items():
                for i, fortress in enumerate(points["fortresses"]):
                    owner = territory_owners[kingdom]["fortresses"][i]
                    Color(*fortress_colors[owner])  # Используем цвет владельца
                    fort_x = fortress[0] + self.map_pos[0] - 10  # Смещаем по X
                    fort_y = fortress[1] + self.map_pos[1] - 10  # Смещаем по Y

                    # Сохраняем прямоугольник и владельца для проверки касания
                    fort_rect = (fort_x, fort_y, 20, 20)  # (x, y, width, height)
                    self.fortress_rectangles.append((fort_rect, fortress, owner))

                    # Рисуем крепость
                    Ellipse(pos=(fort_x + 10, fort_y + 10), size=(20, 20))  # Центрируем крепость

    def check_fortress_click(self, touch):
        # Проверяем, была ли нажата крепость
        for fort_rect, fortress_pos, owner in self.fortress_rectangles:
            if (fort_rect[0] <= touch.x <= fort_rect[0] + fort_rect[2] and
                    fort_rect[1] <= touch.y <= fort_rect[1] + fort_rect[3]):
                popup = FortressInfoPopup(kingdom=self.current_player_kingdom, fortress_coords=fortress_pos)
                popup.open()

                print(f"Крепость {fortress_pos} принадлежит {'вашему' if owner == self.current_player_kingdom else 'чужому'} королевству!")

                if owner == self.current_player_kingdom:
                    self.open_player_fortress_options(fortress_pos)
                else:
                    self.open_enemy_fortress_options(fortress_pos)

    def open_player_fortress_options(self, fortress_pos):
        # Здесь добавьте логику для открытия окна с возможностями для своих крепостей
        print(f"Открыто окно с возможностями для крепости {fortress_pos} вашего королевства.")

    def open_enemy_fortress_options(self, fortress_pos):
        # Здесь добавьте логику для открытия окна с возможностями для чужих крепостей
        print(f"Открыто окно с возможностями для крепости {fortress_pos} чужого королевства.")

    def on_touch_down(self, touch):
        # Запоминаем начальную точку касания
        if touch.is_mouse_scrolling:
            return  # Игнорируем скроллинг
        self.touch_start = touch.pos

    def on_touch_move(self, touch):
        # Двигаем карту при перемещении касания
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

        # Обновляем позиции крепостей
        for index, (fort_rect, fortress_pos, owner) in enumerate(self.fortress_rectangles):
            fort_x = fortress_pos[0] + self.map_pos[0] - 10  # Смещаем по X
            fort_y = fortress_pos[1] + self.map_pos[1] - 10  # Смещаем по Y
            self.fortress_rectangles[index] = ((fort_x, fort_y, 20, 20), fortress_pos, owner)  # Обновляем прямоугольник

        # Очищаем canvas и снова рисуем карту и крепости
        self.canvas.clear()
        self.draw_map()  # Вызываем отрисовку карты
        self.draw_fortresses()  # Вызываем отрисовку крепостей с новыми позициями

    def on_touch_up(self, touch):
        # Обрабатываем отпускание касания
        if touch.is_mouse_scrolling:
            return  # Игнорируем скроллинг
        self.check_fortress_click(touch)

    def draw_map(self):
        with self.canvas:
            Rectangle(source='files/map/map.png', pos=self.map_pos, size=(screen_width, screen_height))


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

        # Фон выбора княжества
        self.add_widget(Image(source='files/menu.jpg', allow_stretch=True, keep_ratio=False))

        # Заголовок с черным цветом текста
        self.kingdom_label = Label(
            text="Выберите княжество",
            font_size='30sp',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.85},
            color=(0, 0, 0, 1)  # Черный текст
        )
        self.add_widget(self.kingdom_label)

        # Боковая панель для кнопок выбора княжеств
        self.kingdom_buttons = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.4, 0.5),
            pos_hint={'center_x': 0.4, 'center_y': 0.5}
        )

        # Создание кнопок для каждого княжества
        for kingdom in kingdom_points.keys():
            btn = Button(text=kingdom, size_hint=(1, None), height=40)
            btn.bind(on_press=self.select_kingdom)
            self.kingdom_buttons.add_widget(btn)

        self.add_widget(self.kingdom_buttons)

        # Изображение советника
        self.advisor_image = Image(
            source='files/null.png',
            size_hint=(0.3, 0.3),
            pos_hint={'center_x': 0.8, 'center_y': 0.6}  # Позиция изображения
        )
        self.add_widget(self.advisor_image)

        # Описание княжества в текстовом боксе
        self.kingdom_info_box = TextInput(
            text="",
            size_hint=(0.35, None),
            height=120,
            pos_hint={'center_x': 0.8, 'center_y': 0.35},  # Понижаем позицию
            background_color=(0, 0, 0, 1),  # Черный фон
            foreground_color=(1, 1, 1, 1),  # Белый текст
            readonly=True,  # Отключение редактирования
            multiline=True  # Многострочный текст
        )
        self.add_widget(self.kingdom_info_box)

        # Кнопка для начала игры
        self.start_game_button = Button(
            text="Начать игру",
            size_hint=(0.4, None),
            height=70,
            pos_hint={'center_x': 0.8, 'center_y': 0.15}
        )
        self.start_game_button.bind(on_press=self.start_game)
        self.add_widget(self.start_game_button)

    def select_kingdom(self, instance):
        selected_kingdom = instance.text
        self.kingdom_info_box.text = self.get_kingdom_info(selected_kingdom)

        # Сохраняем выбранное княжество
        app = App.get_running_app()
        app.selected_kingdom = selected_kingdom  # Сохранение в атрибут

        # Получение изображения советника
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
            "Селестия": "Селестия - юго-западное княжество.\n"
                        "Экономика: 7\n"
                        "Армия: 7\n"
                        "Дипломатия: 7\n",
            "Хиперион": "Хиперион - средиземная империя.\n"
                        "Экономика: 8\n"
                        "Армия: 10\n"
                        "Дипломатия: 3\n",
            "Халидон": "Халидон - юго-восточное княжество.\n"
                       "Экономика: 6\n"
                       "Армия: 5\n"
                       "Дипломатия: 10\n",
            "Этерия": "Этерия - восточное княжество.\n"
                      "Экономика: 6\n"
                      "Армия: 6\n"
                      "Дипломатия: 9\n"
        }
        return info.get(kingdom, "")

    def start_game(self, instance):
        app = App.get_running_app()
        selected_kingdom = app.selected_kingdom
        if selected_kingdom is None:
            print("Фракция не выбрана. Пожалуйста, выберите фракцию перед началом игры.")
            return

        # Передаем выбранное княжество на новый экран игры
        game_screen = GameScreen(selected_kingdom)
        app.root.clear_widgets()
        app.root.add_widget(MapWidget(selected_kingdom=selected_kingdom, player_kingdom=selected_kingdom))  # Передаем выбранное княжество
        app.root.add_widget(game_screen)



# Основное приложение
class EmpireApp(App):
    def build(self):
        return MenuWidget()

class Main(App):
    def __init__(self, **kwargs):
        super(EmpireApp, self).__init__(**kwargs)# Запуск приложения
        self.selected_kingdom = None  # Инициализация атрибутаif __name__ == '__main__':
    EmpireApp().run()
