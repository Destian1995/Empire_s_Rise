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
        self.units_file = 'files/config/arms/arms.json'  # Путь к файлу юнитов

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

        unit_data = {
            'name': unit_name,
            'count': quantity,
        }
        # Запись данных в файл
        with open(self.resources_file, 'w') as file:
            json.dump(resources_data, file)

        with open(self.units_file, 'w') as file:
            json.dump(unit_data, file)

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


def load_image_data():
    """Загружает информацию об изображениях юнитов из image.json."""
    image_json_path = 'files/config/arms/image.json'

    # Проверка существования файла
    if not os.path.exists(image_json_path):
        raise FileNotFoundError(f"Файл {image_json_path} не найден.")

    # Проверка на пустой файл
    if os.path.getsize(image_json_path) == 0:
        raise ValueError(f"Файл {image_json_path} пустой.")

    with open(image_json_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Ошибка при чтении файла {image_json_path}: {e}")


def load_units_data(faction):
    """Загружает информацию о юнитах для указанной фракции из arms.json."""
    with open('files/config/arms/arms.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        print(f"Название: {data['name']}")
        print(f"Количество: {data['count']}")
        return data.get(faction, {})


def show_army_headquarters(faction):
    """Показать окно генштаба с информацией о юнитах."""
    unit_data = load_units_data(faction)
    english_faction = faction_translation.get(faction, faction)

    # Загрузка данных о путях к изображениям из image.json
    image_data = load_image_data()

    unit_popup = Popup(title="Генштаб", size_hint=(0.9, 0.9))

    # Создаем основной layout
    main_layout = BoxLayout(orientation='vertical')

    # Верхний апплет для не расквартированных юнитов
    unassigned_layout = BoxLayout(orientation='vertical', size_hint_y=0.5, padding=(10, 10, 10, 10))

    unassigned_label = Label(text="Не расквартированные юниты", size_hint_y=None, height=40)
    unassigned_layout.add_widget(unassigned_label)

    # Цикл по юнитам, чтобы создать элементы интерфейса для каждого юнита
    for unit_name, unit_info in unit_data.items():
        if 'count' not in unit_info:
            print(f"Ошибка: информация о юните '{unit_name}' не содержит 'count'")
            continue  # Пропускаем данный юнит, если отсутствует количество

        unit_image = image_data.get(english_faction, {}).get(unit_name, "files/army/default.jpg")

        unit_icon = Image(source=unit_image, size_hint=(0.2, 1))
        unit_count = Label(text=f"Количество: {unit_info['count']}", size_hint=(0.2, 1))

        garrison_button = Button(text="Расквартировать", size_hint=(0.2, 1))
        garrison_button.bind(on_release=lambda instance, name=unit_name, count=unit_info['count']: garrison_units(name, count))

        unit_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        unit_box.add_widget(unit_icon)
        unit_box.add_widget(unit_count)
        unit_box.add_widget(garrison_button)

        unassigned_layout.add_widget(unit_box)

    main_layout.add_widget(unassigned_layout)

    # Нижний апплет для расквартированных юнитов
    assigned_layout = BoxLayout(orientation='vertical', size_hint_y=0.5, padding=(10, 10, 10, 10))
    assigned_label = Label(text="Расквартированные юниты", size_hint_y=None, height=40)
    assigned_layout.add_widget(assigned_label)

    # Здесь можно добавить логику отображения расквартированных юнитов
    main_layout.add_widget(assigned_layout)

    unit_popup.content = main_layout
    unit_popup.open()


def garrison_units(unit_name, available_count):
    """Обрабатывает расквартирование юнитов."""
    garrison_popup = Popup(title="Выбор города", size_hint=(0.8, 0.4))

    # Список городов, в которых можно расквартировать юниты (пример)
    cities = ["Город 1", "Город 2", "Город 3"]

    city_layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10))

    city_label = Label(text=f"Расквартировать {unit_name}, доступно: {available_count}", size_hint_y=None, height=40)
    city_layout.add_widget(city_label)

    # Создаем выпадающий список для выбора города
    city_dropdown = TextInput(hint_text="Введите название города", size_hint_y=None, height=40)
    city_layout.add_widget(city_dropdown)

    # Поле ввода для количества юнитов
    quantity_input = TextInput(hint_text="Количество юнитов", size_hint_y=None, height=40)
    city_layout.add_widget(quantity_input)

    def confirm_garrison(instance):
        """Подтверждает расквартирование юнитов."""
        city_name = city_dropdown.text
        quantity = quantity_input.text
        if not city_name or not quantity.isdigit() or int(quantity) <= 0:
            print("Введите корректные данные.")
            return

        quantity = int(quantity)
        if quantity > available_count:
            print("Недостаточно юнитов для расквартирования.")
            return

        # Логика для расквартирования юнитов
        print(f"{quantity} юнитов {unit_name} расквартированы в {city_name}.")

        garrison_popup.dismiss()

    confirm_button = Button(text="Подтвердить", size_hint_y=None, height=40)
    confirm_button.bind(on_release=confirm_garrison)
    city_layout.add_widget(confirm_button)

    garrison_popup.content = city_layout
    garrison_popup.open()


def start_army_mode(faction, game_area):
    """Инициализация армейского режима для выбранной фракции."""
    army_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})

    train_btn = Button(text="Тренировка войск", size_hint_x=0.33, size_hint_y=None, height=50)
    headquarters_btn = Button(text="Генштаб", size_hint_x=0.33, size_hint_y=None, height=50)
    defend_btn = Button(text="Управление дб. оружием", size_hint_x=0.33, size_hint_y=None, height=50)

    army_layout.add_widget(train_btn)
    army_layout.add_widget(headquarters_btn)
    army_layout.add_widget(defend_btn)
    game_area.add_widget(army_layout)

    train_btn.bind(on_release=lambda x: show_unit_selection(faction))
    headquarters_btn.bind(on_release=lambda x: show_army_headquarters(faction))