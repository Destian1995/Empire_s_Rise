# army.py
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

from game_process import *  # Импортируем GameScreen

faction_translation = {
    "Аркадия": "arkadia",
    "Селестия": "celestia",
    "Этерия": "eteria",
    "Хиперион": "giperion",
    "Халидон": "halidon",
}

def start_army_mode(faction, game_area):
    """Инициализация армейского режима для выбранной фракции"""
    # Кнопки для управления армией
    army_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    train_btn = Button(text="Тренировка войск", size_hint_x=0.33, size_hint_y=None, height=50)
    attack_btn = Button(text="Расквартировка", size_hint_x=0.33, size_hint_y=None, height=50)
    defend_btn = Button(text="Управление дб. оружием", size_hint_x=0.33, size_hint_y=None, height=50)

    army_layout.add_widget(train_btn)
    army_layout.add_widget(attack_btn)
    army_layout.add_widget(defend_btn)

    # Добавляем layout с кнопками в нижнюю часть экрана
    game_area.add_widget(army_layout)

    # Привязываем кнопку "Тренировка войск" к функции показа юнитов
    train_btn.bind(on_release=lambda x: show_unit_selection(faction))

def show_unit_selection(faction):
    """Показать окно выбора юнитов для найма"""
    # Переводим русское название фракции в английское
    english_faction = faction_translation.get(faction, faction)

    # Создаем Popup для выбора юнитов
    unit_popup = Popup(title="Выбор юнитов", size_hint=(0.9, 0.9))

    # Создаем GridLayout для размещения юнитов
    unit_layout = GridLayout(cols=2, padding=10, spacing=10)

    # Создаем TextInput для отображения характеристик юнита
    stats_box = TextInput(readonly=True, size_hint=(0.5, 1))

    # Список юнитов и их стоимости (пример)
    units_arkadia = {
        "Солдат": {
            "cost": (350, 1),
            "image": f"files/army/{english_faction}/soldier.jpg",
            "stats": {
                "Урон против наземных юнитов": 100,
                "Урон против воздушных юнитов": 40,
                "Защита против наземных юнитов": 30,
                "Защита против воздушных юнитов": 30,
                "Живучесть": 100,
                "----------------------------": '',
                "Индекс эффективности": "10 из 50"
            }
        },
        "Броневик": {
            "cost": (750, 7),
            "image": f"files/army/{english_faction}/track.jpg",
            "stats": {
                "Урон против наземных юнитов": 250,
                "Урон против воздушных юнитов": 100,
                "Защита против наземных юнитов": 270,
                "Защита против воздушных юнитов": 90,
                "Живучесть": 250,
                "----------------------------": '',
                "Индекс эффективности": "27 из 50"
            }
        },
        "Артиллерия": {
            "cost": (800, 10),
            "image": f"files/army/{english_faction}/push.jpg",
            "stats": {
                "Урон против наземных юнитов": 700,
                "Урон против воздушных юнитов": 20,
                "Защита против наземных юнитов": 90,
                "Защита против воздушных юнитов": 10,
                "Живучесть": 200,
                "----------------------------": '',
                "Индекс эффективности": "26 из 50"
            }
        },
        "Истребитель": {
            "cost": (3500, 45),
            "image": f"files/army/{english_faction}/istrebitel.jpg",
            "stats": {
                "Урон против наземных юнитов": 350,
                "Урон против воздушных юнитов": 550,
                "Защита против наземных юнитов": 40,
                "Защита против воздушных юнитов": 250,
                "Живучесть": 450,
                "----------------------------": '',
                "Индекс эффективности": "40 из 50"
            }
        },
    }

    # Добавляем юниты в layout
    if english_faction == 'arkadia':
        for unit_name, unit_info in units_arkadia.items():
            # Создаем контейнер для юнита
            unit_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(200, 200))

            # Добавляем изображение юнита
            unit_image = Image(source=unit_info["image"], size_hint=(1, 0.6))  # Уменьшил высоту изображения
            unit_box.add_widget(unit_image)

            # Добавляем информацию о стоимости
            cost_label = Label(text=f"Кроны: {unit_info['cost'][0]} \nРабочие: {unit_info['cost'][1]}",
                               size_hint=(1, 0.2))
            unit_box.add_widget(cost_label)

            # Создаем контейнер для кнопок "Нанять" и "Инфо"
            button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

            # Добавляем кнопку для найма юнита
            hire_btn = Button(text="Нанять", size_hint_x=0.5)
            hire_btn.bind(on_release=lambda x, name=unit_name: hire_unit(name))
            button_layout.add_widget(hire_btn)

            # Добавляем кнопку "Инфо" для показа характеристик юнита
            info_btn = Button(text="Инфо", size_hint_x=0.5)
            info_btn.bind(
                on_release=lambda x, name=unit_name, info=unit_info["stats"]: display_unit_stats_info(name, info,
                                                                                                      stats_box))
            button_layout.add_widget(info_btn)

            # Добавляем кнопку layout в основной контейнер юнита
            unit_box.add_widget(button_layout)

            unit_layout.add_widget(unit_box)


    # Добавляем layout юнитов в Popup
    unit_popup.content = BoxLayout(orientation='horizontal')
    unit_popup.content.add_widget(unit_layout)
    unit_popup.content.add_widget(stats_box)  # Добавляем текстовый бокса

    unit_popup.open()

def display_unit_stats(touch, unit_name, stats, stats_box):
    """Отображает характеристики юнита в текстовом боксе"""
    # Проверяем, произошло ли нажатие на юнит
    if touch.is_mouse_scrolling or not touch.grab_current:
        return

    stats_text = f"{unit_name}\n\n"
    for key, value in stats.items():
        stats_text += f"{key}: {value}\n"
    stats_box.text = stats_text  # Устанавливаем текст характеристик юнита

def display_unit_stats_info(unit_name, stats, stats_box):
    """Отображает характеристики юнита в текстовом боксе при нажатии кнопки 'Инфо'"""
    stats_text = f"{unit_name}:\n\n"
    for key, value in stats.items():
        stats_text += f"{key}: {value}\n"
    stats_box.text = stats_text  # Устанавливаем текст характеристик юнита

def hire_unit(unit_name):
    """Логика для найма юнита"""
    print(f"Юнит {unit_name} нанят!")  # Здесь можно добавить логику для изменения ресурсов

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
