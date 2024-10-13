from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

def start_army_mode(faction, game_area):
    """Инициализация армейского режима для выбранной фракции"""

    # Добавление интерфейса армейского режима
    label = Label(text=f"Армейский режим для {faction}", font_size='20sp', size_hint=(1, 0.1))
    game_area.add_widget(label)

    # Кнопки для управления армией
    army_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))

    train_btn = Button(text="Тренировать войска", size_hint_y=None, height=50)
    attack_btn = Button(text="Атаковать врага", size_hint_y=None, height=50)
    defend_btn = Button(text="Защищать территорию", size_hint_y=None, height=50)

    army_layout.add_widget(train_btn)
    army_layout.add_widget(attack_btn)
    army_layout.add_widget(defend_btn)

    game_area.add_widget(army_layout)
