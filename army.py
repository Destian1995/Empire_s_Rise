# army.py
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from game_process import *  # Импортируем GameScreen

def start_army_mode(faction, game_area):
    """Инициализация армейского режима для выбранной фракции"""



    # Кнопки для управления армией
    army_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    train_btn = Button(text="Тренировать войска", size_hint_x=0.33, size_hint_y=None, height=50)
    attack_btn = Button(text="Атаковать врага", size_hint_x=0.33, size_hint_y=None, height=50)
    defend_btn = Button(text="Защищать территорию", size_hint_x=0.33, size_hint_y=None, height=50)

    army_layout.add_widget(train_btn)
    army_layout.add_widget(attack_btn)
    army_layout.add_widget(defend_btn)

    # Добавляем layout с кнопками в нижнюю часть экрана
    game_area.add_widget(army_layout)

def switch_to_economy(faction, game_area):
    import economic  # Импортируем здесь, чтобы избежать циклического импорта
    game_area.clear_widgets()
    economic.start_economy_mode(faction, game_area)

def switch_to_army(faction, game_area):
    import army  # Импортируем здесь, чтобы избежать циклического импорта
    game_area.clear_widgets()
    army.start_army_mode(faction, game_area)

def switch_to_politics(faction, game_area):
    import politic  # Импортируем здесь, чтобы избежать циклического импорта
    game_area.clear_widgets()
    politic.start_politic_mode(faction, game_area)
