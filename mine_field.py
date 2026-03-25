import random

class Game:

    def __init__(self, cols, rows, mines):
        self.cols = cols
        self.rows = rows
        self.mines = mines
        self.game_over = False

        self.hidden_field = self.create_hidden_field()
        self.player_field = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    # Поиск всех соседей клетки
    def neighbors(self, row, col):
        neighbors_list = []
        # определение соседей
        for i in range(-1, 2):
                # пропустить центр
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                # соседи
                nr = row + i
                nc = col + j
                # проверка границ
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors_list.append((nr, nc))         
        return neighbors_list


    # Скрытое от игрока поле
    def create_hidden_field(self):
        # поле, заполненное нулями
        field = [[0] * self.cols for _ in range(self.rows)]

        # Разместить мины
        mines_placed = 0 # размещенные мины

        while mines_placed < self.mines:
            r = random.randint(0, self.rows - 1) # случайный ряд
            c = random.randint(0, self.cols - 1) # случайный столбец

            # проверка, что мины там нет и добавление
            if field[r][c] != -1:
                field[r][c] = -1
                mines_placed += 1

                # Разместить числа
                for nr, nc in self.neighbors(r, c):
                    if field[nr][nc] != -1:
                        field[nr][nc] += 1

        return field
    

    # Проверка победы
    # Если не осталось закрытых кроме мин, игра окончена
    def check_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if (self.hidden_field[row][col] != -1 and not self.player_field[row][col]): 
              #  or \ (self.hidden_field[row][col] == -1 and not self.flags[row][col]):
                    return False
        return True
    
    
    # Открыть клетку
    def open_cell(self, row, col):
        if not(0 <= row < self.rows and 0 <= col < self.cols):
            return 'INVALID_COORDS'     # координаты не существуют
        elif self.flags[row][col]:
            return 'HAS_FLAG'           # уже стоит флаг
        elif self.player_field[row][col]:
            return 'ALREADY_OPEN'       # уже открыта клетка
        elif self.hidden_field[row][col] == -1:
            self.game_over = True       
            return 'MINE'               # в клетке мина
        
        cell_value = self.hidden_field[row][col] # значение в клетке
        self.player_field[row][col] = True # клетка открыта

        # Если 0, нужно открыть все клетки до тех, где есть цифры
        if cell_value == 0:
            for nr, nc in self.neighbors(row, col):
                if not(self.player_field[nr][nc]) and not(self.flags[nr][nc]): 
                    self.open_cell(nr, nc)
        
        if self.check_win():
            self.game_over = True
        return 'OK'


    # Смена флага
    def toggle_flag(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if not (self.player_field[row][col]):
                if self.flags[row][col]:
                    self.flags[row][col] = False
                else:  
                    self.flags[row][col] = True
