# army.py
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from functools import partial
import json
import os

faction_translation = {
    "Аркадия": "arkadia",
    "Селестия": "celestia",
    "Этерия": "eteria",
    "Хиперион": "giperion",
    "Халидон": "halidon",
}

# Класс для управления ресурсами армии
class ArmyCash:
    def __init__(self, faction):
        self.faction = faction
        self.resources_file = 'files/config/resources/resources.json'  # Путь к файлу ресурсов

    def hire_unit(self, unit_name, unit_cost, quantity):
        """Записывает ресурсы для найма юнита в файл."""
        crowns, workers = unit_cost  # Извлекаем стоимость юнита
        required_crowns = int(crowns) * int(quantity)  # Рассчитываем общее количество необходимых крон
        required_workers = int(workers) * int(quantity)  # Рассчитываем общее количество необходимых рабочих

        # Сохраняем информацию о необходимых ресурсах в файл
        resources_data = {
            'crowns': required_crowns,
            'workers': required_workers
        }

        # Запись данных в файл
        with open(self.resources_file, 'w') as file:
            json.dump(resources_data, file)

        print(f"Юнит {unit_name} нанят! Необходимые ресурсы: {resources_data}.")
        return True  # Возвращаем успех


def load_unit_data(faction):
    """Загружает данные о юнитах для выбранной фракции из JSON-файла"""
    english_faction = faction_translation.get(faction, faction)
    file_path = f"files/config/units/{english_faction}.json"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл с юнитами для фракции {faction} не найден.")
        return {}


def show_unit_selection(faction):
    """Показать окно выбора юнитов для найма"""
    english_faction = faction_translation.get(faction, faction)
    unit_data = load_unit_data(english_faction)

    unit_popup = Popup(title="Выбор юнитов", size_hint=(0.9, 0.9))
    scroll_view = ScrollView(size_hint=(0.6, 1))

    unit_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None)
    unit_layout.bind(minimum_height=unit_layout.setter('height'))

    stats_box = TextInput(readonly=True, size_hint=(0.3, 1), padding=(20, 10, 20, 10))
    army_hire = ArmyCash(faction)  # Создаем экземпляр ArmyCash

    for unit_name, unit_info in unit_data.items():
        unit_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(200, 200))

        unit_image = Image(source=unit_info["image"], size_hint=(1, 0.6))
        unit_box.add_widget(unit_image)

        cost_label = Label(text=f"Кроны: {unit_info['cost'][0]} \nРабочие: {unit_info['cost'][1]}",
                           size_hint=(1, 0.2))
        unit_box.add_widget(cost_label)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        hire_btn = Button(text="Нанять", size_hint_x=0.5)

        # Создаем TextInput для ввода количества юнитов внутри цикла
        quantity_input = TextInput(hint_text="Количество", size_hint_x=0.5)

        # Обновленный вызов hire_units
        hire_btn.bind(on_release=lambda instance, name=unit_name, cost=unit_info['cost'], input_box=quantity_input: hire_units(name, cost, input_box, army_hire))

        button_layout.add_widget(hire_btn)
        button_layout.add_widget(quantity_input)

        info_btn = Button(text="Инфо", size_hint_x=0.5)
        info_btn.bind(
            on_release=lambda x, name=unit_name, info=unit_info["stats"]: display_unit_stats_info(name, info, stats_box))
        button_layout.add_widget(info_btn)

        unit_box.add_widget(button_layout)
        unit_layout.add_widget(unit_box)

    scroll_view.add_widget(unit_layout)

    popup_content = BoxLayout(orientation='horizontal', padding=(10, 10, 10, 10))
    popup_content.add_widget(scroll_view)
    popup_content.add_widget(stats_box)

    unit_popup.content = popup_content
    unit_popup.open()

def hire_units(unit_name, unit_cost, quantity_input, army_hire):
    """Обрабатывает найм юнитов и проверяет количество."""
    quantity_text = quantity_input.text  # Получаем текст из поля ввода

    try:
        # Проверяем, не пустое ли поле
        if not quantity_text:
            print("Введите количество юнитов.")
            return

        quantity = int(quantity_text)

        if quantity <= 0:
            print("Количество должно быть больше нуля.")
            return

        # Теперь faction доступен в army_hire, так как он был создан при инициализации
        if army_hire.hire_unit(unit_name, unit_cost, quantity):
            print(f"{quantity} юнитов {unit_name} наняты!")
        else:
            print(f"Не удалось нанять {quantity} юнитов {unit_name} из-за недостатка ресурсов.")

    except ValueError:
        print("Введите корректное количество.")


def display_unit_stats_info(unit_name, stats, stats_box):
    """Отображает характеристики юнита в текстовом боксе при нажатии кнопки 'Инфо'"""
    stats_text = f"{unit_name}:\n\n"
    for key, value in stats.items():
        stats_text += f"{key}: {value}\n"
    stats_box.text = stats_text  # Устанавливаем текст характеристик юнита


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


def start_army_mode(faction, game_area):
    """Инициализация армейского режима для выбранной фракции"""
    army_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    train_btn = Button(text="Тренировка войск", size_hint_x=0.33, size_hint_y=None, height=50)
    attack_btn = Button(text="Расквартировка", size_hint_x=0.33, size_hint_y=None, height=50)
    defend_btn = Button(text="Управление дб. оружием", size_hint_x=0.33, size_hint_y=None, height=50)

    army_layout.add_widget(train_btn)
    army_layout.add_widget(attack_btn)
    army_layout.add_widget(defend_btn)
    game_area.add_widget(army_layout)

    train_btn.bind(on_release=lambda x: show_unit_selection(faction))