

### План разработки пошаговой глобальной стратегии:

1. **Структура проекта**
   - Основные файлы проекта:
     - `main.py` — меню игры, выбор фракции и запуск карты(процесс game_process.py).
     - `game_process.py` - цикл игры который обрабатывает действия игрока и переключает между собой фракции управляемые ИИ(ИИ делает набор действий и завершает ход передавая право хода следующей фракции и так пока снова не настанет очередь игрока). Включает в себя интерфейс с кнопками который запускает отдельные файлы py(они переключают режим карты, который дает доступ к определенным наборам кнопок) economic.py, army.py. politic.py, именно с помощью них игрок и ИИ выполняют действия в игре.
     - `economic.py` — режим карты экономика (строительство зданий, торговля, налоги).
     - `army.py` — режим карты армия (создание войск, ведение войн).
     - `events.py` — случайные события (как позитивные, так и негативные).
     - `politic.py` - режим карты открывающий набор кнопок для заключения союзов и договоров.
     - `resources.py` — управление ресурсами (деньги, люди).
     - `ui.py` — интерфейс городов.
     - **`ii.py`** — логика ИИ для управления действиями других княжеств.
   
2. **ИИ княжеств**
   - **Логика действий ИИ:**
     - ИИ должен также управлять своими ресурсами (деньги, люди), строить экономические и военные здания.
     - Принятие решений о торговле с другими княжествами, включая игрока (заключение договоров, торговые пути).
     - Взаимодействие с игроком через дипломатические акции (альянсы, объявления войны).
     - ИИ может агрессивно расширять свои территории или строить более мирную экономическую политику.
   
3. **Разработка ИИ (в файле `ii.py`)**
   - **Анализ состояния ресурсов:**
     - ИИ регулярно оценивает количество денег и людей для принятия решений о строительстве зданий или армий.
   
   - **Действия ИИ:**
     - Постройка зданий, формирование армии в зависимости от текущего состояния княжества.
     - Торговля: ИИ заключает торговые сделки с игроком или другими ИИ княжествами.
     - Война: Если ресурсы позволяют и ситуация на карте выгодна, ИИ может начать военные действия против игрока или других княжеств.
   
   - **Случайные факторы:**
     - ИИ может по-разному реагировать на случайные события (сохранять нейтралитет, использовать возможность для расширения или обороны).

4. **Геймплей с ИИ**
   - Игрок взаимодействует с ИИ-княжествами, заключая мирные соглашения или вступая в войны.
   - Княжества под управлением ИИ могут влиять на баланс сил в игре, усложняя жизнь игроку или помогая в достижении целей.

---

