# economic.py
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from game_process import *  # Импортируем GameScreen

def start_economy_mode(faction, game_area):
    """Инициализация экономического режима для выбранной фракции"""



    # Кнопки для управления экономикой
    economy_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    build_btn = Button(text="Построить здание", size_hint_x=0.33, size_hint_y=None, height=50)
    trade_btn = Button(text="Торговать", size_hint_x=0.33, size_hint_y=None, height=50)
    expand_btn = Button(text="Расширить территорию", size_hint_x=0.33, size_hint_y=None, height=50)

    economy_layout.add_widget(build_btn)
    economy_layout.add_widget(trade_btn)
    economy_layout.add_widget(expand_btn)

    # Добавляем layout с кнопками в нижнюю часть экрана
    game_area.add_widget(economy_layout)

def switch_to_army(faction, game_area):
    import army  # Импортируем здесь, чтобы избежать циклического импорта
    game_area.clear_widgets()
    army.start_army_mode(faction, game_area)

def switch_to_politics(faction, game_area):
    import politic  # Импортируем здесь, чтобы избежать циклического импорта
    game_area.clear_widgets()
    politic.start_politic_mode(faction, game_area)

def switch_to_economy(faction, game_area):
    import economic  # Импортируем здесь, чтобы избежать циклического импорта
    game_area.clear_widgets()
    economic.start_economy_mode(faction, game_area)
