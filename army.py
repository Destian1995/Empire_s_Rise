# army.py
from kivy.graphics.svg import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from functools import partial
import json
import os
import time


faction_translation = {
    "Аркадия": "arkadia",
    "Селестия": "celestia",
    "Этерия": "eteria",
    "Хиперион": "giperion",
    "Халидон": "halidon",
}

class ArmyCash:
    def __init__(self, faction):
        self.faction = faction
        self.resources_file = 'files/config/resources/resources.json'
        self.cash_resources = 'files/config/resources/cash.json'
        self.units_file = 'files/config/arms/arms.json'  # Путь к файлу юнитов
        self.resources = self.load_resources()

    def load_resources(self):
        """Загружает состояние ресурсов из файла."""
        if os.path.exists(self.cash_resources):
            with open(self.cash_resources, 'r') as file:
                try:
                    resources = json.load(file)  # Читаем данные один раз
                    print(resources)  # Печатаем загруженные ресурсы
                    return resources  # Возвращаем загруженные данные
                except json.JSONDecodeError:
                    print("Ошибка при загрузке ресурсов: файл пуст или повреждён.")

    def hire_unit(self, unit_name, unit_cost, quantity, image_unit):
        """Нанимает юнита, если ресурсов достаточно."""
        crowns, workers = unit_cost  # Извлекаем стоимость юнита
        required_crowns = int(crowns) * int(quantity)  # Рассчитываем общее количество необходимых крон
        required_workers = int(workers) * int(quantity)  # Рассчитываем общее количество необходимых рабочих

        # Проверяем, хватает ли ресурсов
        if self.resources['Кроны'] < required_crowns or self.resources['Рабочие'] < required_workers:
            print(f"Нанять юнитов невозможно: недостаточно ресурсов. Необходимые: {required_crowns} крон и {required_workers} рабочих.")
            return False  # Не хватает ресурсов для найма

        # Если ресурсов достаточно, обновляем их
        self.resources['Кроны'] -= required_crowns
        self.resources['Рабочие'] -= required_workers
        with open(self.cash_resources, 'w') as file:
            json.dump(self.resources, file, ensure_ascii=False, indent=4)  # Запись с индентацией для удобства

        # Чтение существующих юнитов из файла
        units_data = {}
        if os.path.exists(self.units_file):
            with open(self.units_file, 'r') as file:
                try:
                    units_data = json.load(file)
                except json.JSONDecodeError:
                    units_data = {}

        # Обновление или добавление юнита
        if image_unit in units_data:
            units_data[image_unit]['count'] += quantity  # Увеличиваем количество юнитов
        else:
            units_data[image_unit] = {
                'name': unit_name,
                'count': quantity,
                'image': image_unit,
            }

        # Запись обновлённых данных о юнитах в файл
        with open(self.units_file, 'w') as file:
            json.dump(units_data, file)

        print(f"Юнит {unit_name} нанят! Необходимые ресурсы: {required_crowns} крон и {required_workers} рабочих.")
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

        # Вызов hire_units с передачей ссылки на изображение
        hire_btn.bind(on_release=lambda instance, name=unit_name, cost=unit_info['cost'],
                                        input_box=quantity_input, img=unit_info['image']: hire_units(name, cost, input_box, army_hire, img))

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

def hire_units(unit_name, unit_cost, quantity_input, army_hire, image):
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

        # Передача ссылки на изображение юнита в функцию hire_unit
        if army_hire.hire_unit(unit_name, unit_cost, quantity, image):
            print(f"{quantity} юнитов {unit_name} наняты! Ссылка на изображение: {image}")
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


# Функция для загрузки информации о юнитах
def load_units_data(faction):
    with open('files/config/arms/arms.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get(faction, {})

# Функция для загрузки информации об изображениях
def load_image_data(faction):
    with open('files/config/arms/image.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get(faction, {})


class GeneralStaff:
    def __init__(self, faction):
        self.faction = faction
        self.garrison_file = f'files/config/garrison/{faction_translation[faction]}.json'
        self.units = {}  # Хранение информации о юнитах

        # Загрузка данных о расквартированных юнитах
        self.load_garrison_data()

    def load_garrison_data(self):
        """Загружает данные о расквартированных юнитах из файла."""
        if os.path.exists(self.garrison_file):
            with open(self.garrison_file, 'r', encoding='utf-8') as file:
                self.units = json.load(file)
        else:
            self.units = {}  # Если файл не найден, создаем пустой словарь

    def save_garrison_data(self):
        """Сохраняет текущие данные о расквартированных юнитах в файл."""
        with open(self.garrison_file, 'w', encoding='utf-8') as file:
            json.dump(self.units, file)

    def garrison_units(self, unit_name, city, count):
        """Расквартировать юнитов в указанный город."""
        if city not in self.units:
            self.units[city] = {}
        if unit_name in self.units[city]:
            self.units[city][unit_name] += count
        else:
            self.units[city][unit_name] = count

        # Сохраняем обновленные данные
        self.save_garrison_data()

        print(f"{count} юнитов {unit_name} расквартированы в {city}.")

    def move_units(self, unit_name, from_city, to_city, count):
        """Перемещает юниты из одного города в другой."""
        if from_city in self.units and unit_name in self.units[from_city]:
            if self.units[from_city][unit_name] >= count:
                # Уменьшаем количество юнитов в исходном городе
                self.units[from_city][unit_name] -= count
                if self.units[from_city][unit_name] == 0:
                    del self.units[from_city][unit_name]

                # Перемещаем юниты в новый город
                self.garrison_units(unit_name, to_city, count)

                print(f"{count} юнитов {unit_name} перемещены из {from_city} в {to_city}.")
                return True
            else:
                print(f"Недостаточно юнитов {unit_name} в {from_city}.")
                return False
        else:
            print(f"Юнит {unit_name} не найден в {from_city}.")
            return False

    def get_garrisoned_units(self, city):
        """Возвращает список юнитов, расквартированных в указанном городе."""
        return self.units.get(city, {})

def load_units_data():
    """Загружает данные юнитов из файла arms.json."""
    units_data = {}
    units_file_path = 'files/config/arms/arms.json'  # Путь к файлу юнитов

    if os.path.exists(units_file_path):
        with open(units_file_path, 'r', encoding='utf-8') as file:
            units_data = json.load(file)

    return units_data

def show_army_headquarters(faction):
    """Показать окно Генштаба с информацией о юнитах."""
    general_staff = GeneralStaff(faction)  # Создаем объект Генштаба

    # Загрузка данных о юнитах
    units_data = load_units_data()

    unit_popup = Popup(title="Генштаб", size_hint=(0.9, 0.9))

    # Создаем TabbedPanel
    tab_panel = TabbedPanel(do_default_tab=False)

    # Вкладка для нерасквартированных юнитов
    unassigned_tab = TabbedPanelItem(text="Не расквартированные юниты")
    unassigned_layout = GridLayout(cols=3, padding=(10, 10, 10, 10), size_hint_y=None)
    unassigned_layout.bind(minimum_height=unassigned_layout.setter('height'))
    scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
    scroll_view.add_widget(unassigned_layout)

    # Цикл по юнитам для отображения их изображений и численности
    for image, unit_info in units_data.items():
        unit_count = unit_info.get('count', 0)

        # Бокс для юнита
        unit_box = BoxLayout(orientation='vertical', size_hint_y=None, height=150)

        # Добавляем изображение юнита, если оно есть
        if image and os.path.exists(image):
            unit_image = Image(source=image)
            unit_box.add_widget(unit_image)
        else:
            unit_box.add_widget(Label(text="Изображение не найдено"))

        # Под изображением выводим численность юнита
        unit_label = Label(text=f"{unit_info['name']}: {unit_count} юнитов")
        unit_box.add_widget(unit_label)

        unassigned_layout.add_widget(unit_box)

    unassigned_tab.add_widget(scroll_view)
    tab_panel.add_widget(unassigned_tab)

    # Вкладка для расквартированных юнитов
    assigned_tab = TabbedPanelItem(text="Расквартированные юниты")
    assigned_layout = BoxLayout(orientation='vertical', padding=(10, 10, 10, 10))
    assigned_tab.add_widget(assigned_layout)

    # Логика отображения расквартированных юнитов по городам
    for city, units in general_staff.units.items():
        city_label = Label(text=f"Город: {city}")
        assigned_layout.add_widget(city_label)
        for unit_name, count in units.items():
            assigned_unit_label = Label(text=f"{unit_name}: {count} юнитов")
            assigned_layout.add_widget(assigned_unit_label)

    tab_panel.add_widget(assigned_tab)

    # Установка одинакового размера для всех вкладок
    tab_panel.bind(width=lambda instance, value: setattr(tab_panel, 'tab_width', value / len(tab_panel.tab_list)))

    # Встраиваем TabPanel в основное окно
    unit_popup.content = tab_panel
    unit_popup.open()


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