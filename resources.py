import economic

class ResourceManager:
    def __init__(self, faction):
        self.faction = faction
        self.money = 250
        self.free_people = 30
        self.food = 400
        self.population = 40
        self.resources = {
            "Деньги": self.money,
            "Свободные люди": self.free_people,
            "Еда": self.food,
            "Население": self.population
        }
        self.economic_params = {
            "Аркадия": {
                "hospital": {"gain_people": 90, "cost_money": 250},
                "factory": {"gain_food": 220, "cost_people": 30},
                "food_consumption": 1.8,
                "tax_rate": 9  # Ставка налога
            },
            "Селестия": {
                "hospital": {"gain_people": 70, "cost_money": 220},
                "factory": {"gain_food": 240, "cost_people": 35},
                "food_consumption": 1.8,
                "tax_rate": 7
            },
            "Хиперион": {
                "hospital": {"gain_people": 110, "cost_money": 220},
                "factory": {"gain_food": 230, "cost_people": 40},
                "food_consumption": 1.7,
                "tax_rate": 7
            },
            "Этерия": {
                "hospital": {"gain_people": 140, "cost_money": 200},
                "factory": {"gain_food": 200, "cost_people": 50},
                "food_consumption": 1.5,
                "tax_rate": 5
            },
            "Халидон": {
                "hospital": {"gain_people": 130, "cost_money": 180},
                "factory": {"gain_food": 200, "cost_people": 70},
                "food_consumption": 1.2,
                "tax_rate": 3
            },
        }

    def get_income_per_person(self):
        """Получение дохода с одного человека для данной фракции."""
        params = self.economic_params[self.faction]
        return params["tax_rate"]

    def calculate_tax_income(self):
        """Расчет дохода от налогов с учетом ставки налога."""
        tax_rate = self.get_income_per_person()  # Получаем налоговую ставку
        taxes = self.population * (tax_rate / 10)  # Делаем расчёт с использованием этой ставки
        return taxes

    def update_resources(self):
        """Обновление ресурсов на основе фракции"""
        params = self.economic_params[self.faction]

        # Прирост свободных людей от больницы
        self.resources["Свободные люди"] += params["hospital"]["gain_people"]
        self.resources["Население"] += params["hospital"]["gain_people"]
        self.resources["Деньги"] -= params["hospital"]["cost_money"]

        # Прирост еды от фабрики
        self.resources["Еда"] += params["factory"]["gain_food"]
        self.resources["Свободные люди"] -= params["factory"]["cost_people"]

        # Расчет потребления еды
        consumption = self.resources["Население"] * params["food_consumption"]
        self.resources["Еда"] -= consumption

        # Расчет налогов
        self.resources["Деньги"] += self.calculate_tax_income()

    def get_resources(self):
        """Получение текущих ресурсов"""
        return self.resources
