
from win11toast import toast
import csv

# Класс 'цели'
class Goals:
    # Создание списка целей
    def __init__(self):
        self._goals = []

    # Записываем в файл
    def update_file(self):
        data = ['Название цели', 'Итоговая сумма', 'Текущий баланс', 'Категория', 'Статус']
        with open('goals.cvs', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            for row in self._goals:
                file.write(f'{row.name},{row.amount},{row.balance},{row.category},{row.status}\n')

    # Вывод всех целей
    def get_goals(self):
        print('Цели:')
        for goal in self._goals:
            print(f'Цель: {goal.name}, баланс: {goal.balance}, необходимая сумма: {goal.amount}р, категория: {goal.category}, статус: {goal.status} Завершено на {goal.balance / goal.amount * 100}%')
        successful()

    # Вывод конкретной цели !!! не используется
    def get_goal(self, name):
        for goal in self._goals:
            if goal.name == name:
                print(f'Цель: {goal.name}, баланс: {goal.balance}, необходимая сумма: {goal.amount}р, категория: {goal.category}, статус: {goal.status}')

    # Метод изменения баланса
    def balance_update(self, name, value, status):
        for goal in self._goals:
            if goal.name == name:
                if goal.status == 'завершено':
                    return print('Невозможно внести, так как цель была завершена ранее')
                if status == 'up':
                    goal.balance += value
                else:
                    goal.balance -= value
                if goal.balance == goal.amount:
                    print('Вы выполнили план')
                    goal.status = 'завершено'
                elif goal.balance > goal.amount:
                    print(f'Вы превысили необходимую сумму на {goal.amount - goal.balance}')
                    goal.status = 'завершено'
                toast(f'Завершено на {goal.balance / goal.amount * 100}%')
        successful()

    # Добавление цели
    def set_goal(self, goal):
        self._goals.extend(goal)

    # Удаление цели
    def del_goal(self, name):
        for goal in self._goals:
            if goal.name == name:
                self._goals.remove(goal)
        successful()

    goal = property(get_goals, set_goal)

# Класс "цель"
class Goal:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.balance = 0
        self.category = category
        self.status = 'Не завершено'

# Метод выбора категории
def set_category():
    # Выбор категории
    if input('Добавить категорию? (\'y\' для согласия, \'enter\' для продолжения) ') == 'y':
        while True:
            match input('Выберите категорию(1 - работа, 2 - здоровье, 3 - развлеченье)\n'):
                case '1':
                    return 'Работа'
                case '2':
                    return 'Здоровье'
                case '3':
                    return 'Развлеченье'
                case _:
                    print('Введено некорректное число')

    else:
        return 'Без категории'

# Считывание данных из файла, если он есть и создаем файл, если его нет
def start(goals):

    try:
        with open('goals.cvs', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                goal = Goal(row['Название цели'], int(row['Итоговая сумма']), row['Категория'])
                goal.balance = int(row['Текущий баланс'])
                goal.status = row['Статус']
                goals.goal = [goal]

    except FileNotFoundError:
        data = ['Название цели', 'Итоговая сумма', 'Текущий баланс', 'Категория', 'Статус']

        with open('goals.cvs', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    except Exception as e:
        print(e)

# В случае успеха спрашиваем, что делать дальше
def successful():
    print('Успех')
    while True:
        match input('Введите \'1\' - для выхода, \'enter\' - чтобы продолжить '):
            case '1':
                goals.update_file()
                exit()
            case _:
                return main()

# Создаем экземпляр класса 'цели'
goals = Goals()

# Получаем данные из файла
start(goals)

# Основная часть
def main():

    # Метод создание цели
    def create_goal():

        # Создаем необходимые переменные
        name = input('Введите название цели: ')

        # Проверяем введено ли число
        while True:
            amount = input('Введите необходимую сумму: ')
            if amount.isdigit():
                break
            else:
                print('Введено некорректное число')
        category = set_category()

        # Добавляем цель
        goals.goal = [Goal(name, int(amount), category)]

    # Метод изменения баланса
    def update_balance():

        # Создаем необходимые переменные
        name = input('Введите название цели у которой хотите изменить баланс: ')

        # Проверяем введено ли число
        while True:
            value = input('Введите сумму изменений: ')
            if value.isdigit():
                break
            else:
                print('Введено некорректное число')

        # Вносим или снимаем со счета
        while True:
            match input('Введите \'1\' - для того чтобы внести на счет, \'2\' - для снятия со счета '):
                case '1':
                    return goals.balance_update(name, int(value), 'up')
                case '2':
                    return goals.balance_update(name, int(value), 'down')
                case _:
                    print('Введено некорректное число')

    # Основная часть
    while True:
        match input('Введите:\n'
                    '\'1\' - для того чтобы создать цель,\n'
                    '\'2\' - для изменения баланса\n'
                    '\'3\' - для вывода целей\n'
                    '\'4\' - для вывода цели\n'
                    '\'5\' - для удаления цели\n'
                    '\'0\' - для выхода\n'):
            case '1':
                # Создаем новую цель
                create_goal()

            case '2':
                # Обновляем баланс
                update_balance()

            case '3':
                # Выводим список целей
                goals.get_goals()

            case '4':
                # Выводим цель
                goals.get_goal(input('Введите название цели: '))

            case '5':
                # Удаляем цель
                goals.del_goal(input('Введите название цели: '))

            case '0':
                goals.update_file()
                exit()

main()






