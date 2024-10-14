from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

# Файл, который включает режимы игры
import economic
import army
import politic
from ii import AIController

# Список всех фракций
FACTIONS = ["Аркадия", "Селестия", "Хиперион", "Халидон", "Этерия"]

# Класс для кнопки с изображением
class ImageButton(ButtonBehavior, Image):
    pass

class GameScreen(Screen):
    def __init__(self, selected_faction, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.selected_faction = selected_faction
        self.ai_controllers = {}
        self.init_ui()

    def init_ui(self):
        # Верхняя панель с выбранной фракцией
        self.faction_label = Label(
            text=f"{self.selected_faction}",
            font_size='30sp',
            size_hint=(1, 0.1),
            pos_hint={'top': 1},
            color=(0, 0, 0, 1))  # Черный цвет текста
        self.add_widget(self.faction_label)

        # Боковая панель с кнопками режимов
        self.mode_panel = BoxLayout(orientation='vertical', size_hint=(0.2, 1), pos_hint={'x': -0.06, 'y': 0})

        # Уменьшенные иконки
        btn_economy = ImageButton(source='files/status/economy.jpg', size_hint_y=None, height=50, width=50, on_press=self.switch_to_economy)
        btn_army = ImageButton(source='files/status/army.jpg', size_hint_y=None, height=65, width=30, on_press=self.switch_to_army)
        btn_politics = ImageButton(source='files/status/politic.jpg', size_hint_y=None, height=65, width=40, on_press=self.switch_to_politics)

        self.mode_panel.add_widget(btn_economy)
        self.mode_panel.add_widget(btn_army)
        self.mode_panel.add_widget(btn_politics)

        self.add_widget(self.mode_panel)

        # Центральная часть для отображения карты и игрового процесса
        self.game_area = FloatLayout(size_hint=(0.8, 1), pos_hint={'x': 0.2, 'y': 0})
        self.add_widget(self.game_area)

        # Добавляем кнопку "Завершить ход" в правый верхний угол
        end_turn_button = Button(
            text="Завершить ход",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'right': 1, 'top': 1},
            on_press=self.process_turn
        )
        self.add_widget(end_turn_button)

        # Инициализация ИИ для остальных фракций
        self.init_ai_controllers()

    def switch_to_economy(self, instance):
        """Переключение на экономический режим"""
        self.clear_game_area()
        economic.start_economy_mode(self.selected_faction, self.game_area)

    def switch_to_army(self, instance):
        """Переключение на армейский режим"""
        self.clear_game_area()
        army.start_army_mode(self.selected_faction, self.game_area)

    def switch_to_politics(self, instance):
        """Переключение на политический режим"""
        self.clear_game_area()
        politic.start_politic_mode(self.selected_faction, self.game_area)

    def clear_game_area(self):
        """Очистка центральной области"""
        self.game_area.clear_widgets()

    def init_ai_controllers(self):
        """Создание контроллеров ИИ для каждой фракции кроме выбранной"""
        for faction in FACTIONS:
            if faction != self.selected_faction:
                self.ai_controllers[faction] = AIController(faction)

    def process_turn(self, instance=None):
        """Обработка хода игрока и ИИ"""
        # Ход игрока (ожидание действий)
        print(f"Ход {self.selected_faction}")

        # Ходы ИИ для остальных фракций
        for faction, ai_controller in self.ai_controllers.items():
            ai_controller.process_turn()
            print(f"Ход ИИ {faction}")
