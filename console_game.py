from mine_field import Game

# Поле 9х9, 10 мин
game = Game(5, 5, 3)

# Отрисовка поля
def print_field(game):
    print('Варианты действия: 1 - открыть ячейку, 2 - поставить флаг')
    print('   ', end = ' ')
    # Номера колонок
    for col in range(game.cols):
        print(col + 1, end =' ')
    print()                 # перевод строки
    for row in range(game.rows):
        # Номера строк
        print(f'{row + 1}  ', end = ' ')
        for col in range(game.cols):
            if game.flags[row][col]: 
                print('F', end = ' ') # флаг
            elif not game.player_field[row][col]:
                print('#', end = ' ') # закрытая
            elif game.player_field[row][col]:
                print(game.hidden_field[row][col], end = ' ') # открытие
            
        print() 

# Ввод данных в консоль
def get_input():
    while True:
        input_list = []
        for el in input('Введите ряд, столбец и действие через пробел: ').split():
            input_list.append(int(el))
        
        # Проверка, что значений 3
        if len(input_list) != 3:
            print(f'Должно быть 3 значения: ряд, столбец и действие!')
            continue

        # Проверка ввода действия
        if input_list[2] != 1 and input_list[2] != 2:
            print(f'Выбран неверный вариант действия. \n'
                'Пожалуйста, выберите действие: \n'
                '1 - открыть клетку, 2 - поставить флаг')
            continue
            
        else:
            row = input_list[0] -1
            col = input_list[1] -1
            action = input_list[2]

        return row, col, action

# Основной цикл
def main(game):
    print_field(game)

    while not game.game_over:
        row, col, action = get_input()

        # Обработка открытия
        if action == 1:
            result = game.open_cell(row, col)
            if result == 'INVALID_COORDS':
                print('Введены неверные координаты!')
                continue
            if result == 'HAS_FLAG':
                print('Там стоит флаг! Убери флаг или выбери другую ячейку')
                continue
            if result == 'ALREADY_OPEN':
                print('Эта клетка уже открыта, выбери другую')
                continue
            if result == 'MINE':
                print('БАБАХ!')
                # При проигрыше покаывам поле целиком
                print('   ', end = ' ')
                for col in range(game.cols):
                    print(f'{col + 1}', end =' ')
                print()                 
                for row in range(game.rows):
                    print(f'{row + 1}  ', end = ' ')
                    for col in range(game.cols):
                        val = game.hidden_field[row][col]
                        if val == -1:
                            print('*', end = ' ')
                        else:
                            print(val, end = ' ')
                    print()
                continue
        
        # Обработка смены флага
        if action == 2:
            game.toggle_flag(row, col)

        # Перерисовка поля
        print_field(game)
        
    print('Игра окончена!')

# Запуск
main(game)