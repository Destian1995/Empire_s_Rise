from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def start_politic_mode(faction, game_area):
    """Инициализация политического режима для выбранной фракции"""

    # Добавление интерфейса политического режима
    label = Label(text=f"Политический режим для {faction}", font_size='20sp', size_hint=(1, 0.1))
    game_area.add_widget(label)

    # Кнопки для управления дипломатией
    politic_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))

    ally_btn = Button(text="Заключить альянс", size_hint_y=None, height=50)
    negotiate_btn = Button(text="Переговоры о мире", size_hint_y=None, height=50)
    betray_btn = Button(text="Предать союзника", size_hint_y=None, height=50)

    politic_layout.add_widget(ally_btn)
    politic_layout.add_widget(negotiate_btn)
    politic_layout.add_widget(betray_btn)

    game_area.add_widget(politic_layout)
