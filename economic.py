from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def start_economy_mode(faction, game_area):
    """Инициализация экономического режима для выбранной фракции"""

    # Добавление интерфейса экономического режима
    label = Label(text=f"Экономический режим для {faction}", font_size='20sp', size_hint=(1, 0.1))
    game_area.add_widget(label)

    # Кнопки для управления экономикой
    economy_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))

    build_btn = Button(text="Построить здание", size_hint_y=None, height=50)
    trade_btn = Button(text="Торговать", size_hint_y=None, height=50)
    expand_btn = Button(text="Расширить территорию", size_hint_y=None, height=50)

    economy_layout.add_widget(build_btn)
    economy_layout.add_widget(trade_btn)
    economy_layout.add_widget(expand_btn)

    game_area.add_widget(economy_layout)
