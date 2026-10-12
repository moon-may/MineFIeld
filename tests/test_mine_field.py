import pytest
from mine_field import Game

@pytest.mark.parametrize('cols, rows, row, col, expected', [
                             (3, 3, 1, 1, 8),
                             (3, 3, 0, 0, 3),
                             (3, 3, 2, 1, 5),
                             (5, 5, 2, 2, 8),
                             (5, 5, 1, 1, 8),
                             (5, 5, 4, 2, 5),
                             (5, 5, 4, 4, 3),
                             (1, 1, 0, 0, 0),
                         ])
def test_neighbors_count(cols, rows, row, col, expected):
    '''
    Проверяет количество соседей для клетки (row, col) на поле (cols, rows).
    '''
    game = Game(cols, rows, 0)
    result = game.neighbors(row, col)
    assert len(result) == expected


def test_neighbors_content_corner():
    '''
    Проверяет конкретных соседей для угловой клетки
    '''
    game = Game(3, 3, 0)
    assert set(game.neighbors(0, 0)) == {(0, 1), (1, 0), (1, 1)}


def test_neighbors_content_center():
    '''
    Проверяет конкретных соседей для центральной клетки
    '''
    game = Game(5, 5, 0)
    assert set(game.neighbors(2, 2)) == {
        (1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)
    }


def test_flag():
    '''
    Проверяет установку флага на начальном поле
    '''
    game = Game(3, 3, 1)
    game.toggle_flag(1, 1)
    assert game.flags[1][1] is True


def test_flag_on_open_cell():
    '''
    Проверяет установку флага на открытую клетку. Флаг не должен установиться. 
    '''
    game = Game(3, 3, 0)
    game.player_field[1][0] = True
    game.toggle_flag(1, 0)
    assert game.flags[1][0] is False


def test_flag_on_mine():
    '''
    Проверяет установку флага на поле с миной
    '''
    game = Game(3, 3, 0)
    game.hidden_field[1][1] = -1
    game.toggle_flag(1, 1)
    assert game.flags[1][1] is True


def test_toggle_flag():
    '''
    Проверяет корректность снятия флага
    '''
    game = Game(3, 3, 1)
    game.toggle_flag(1, 1)
    assert game.flags[1][1] is True
    game.toggle_flag(1, 1)
    assert game.flags[1][1] is False


def test_flag_on_bounds():
    '''
    Проверяет устойчивость к некорректным данным. Флаг не должен появиться в другом месте. 
    '''
    game = Game(3, 3, 0)
    game.toggle_flag(10, 10)
    game.toggle_flag(-1, -1)
    assert sum(sum(row) for row in game.flags) == 0


def test_check_win():
    '''
    Проверяет работу чек-бокса победы, когда открыты все клетки кроме клеток с минами
    '''
    game = Game(3, 3, 1)
    game.hidden_field = [[1, -1, 1],
                         [1, 1, 1],
                         [0, 0, 0]]
    game.player_field = [[True, False, True],
                         [True, True, True],
                         [True, True, True]]
    assert game.check_win()


def test_check_win_negative():
    '''
    Проверяет работу чек-бокса победы, когда открыты не все безопасные клетки
    '''
    game = Game(3, 3, 1)
    game.hidden_field = [[1, -1, 1],
                         [1, 1, 1],                             
                         [0, 0, 0]]
    game.player_field = [[True, False, True],
                         [True, True, True],
                         [False, True, True]]
    assert game.check_win() is False


@pytest.mark.parametrize('row, col', [
    pytest.param(10, 1, id='rows_out_of_bounds'), 
    pytest.param(-5, 0, id='negative_coords'), 
    pytest.param(1, 10, id='cols_out_of_bounds'), 
    pytest.param(0, 9, id='boundary_values')
])
def test_invalid_coords(row, col):
    '''
    Проверяет поведение open_cell при заведомо неверных координатах
    '''
    game = Game(9, 9, 10)
    assert game.open_cell(row, col) == 'INVALID_COORDS'


def test_has_flag():
    '''
    Проверяет поведение open_cell при попытке открыть клетку, отмеченную флагом
    '''
    game = Game(9, 9, 10)
    game.flags[7][2] = True
    assert game.open_cell(7, 2) == 'HAS_FLAG'
    assert game.player_field[7][2] is False 


def test_already_open():
    '''
    Проверяет поведение open_cell при попытке открыть уже открытую клетку
    '''
    game = Game(9, 9, 10)
    game.player_field[5][5] = True
    assert game.open_cell(5, 5) == 'ALREADY_OPEN'


def test_is_mine():
    '''
    Проверяет поведение open_cell при открытии мины
    '''
    game = Game(9, 9, 10)
    game.hidden_field[5][5] = -1
    assert game.open_cell(5, 5) == 'MINE'
    assert game.game_over is True


def test_open_cell():
    '''
    Проверяет поведение open_cell при идеальном сценарии
    '''
    game = Game(9, 9, 0)
    assert game.open_cell(7, 5) == 'OK'
    assert game.player_field[7][5] is True 


def test_open_zero():
    '''
    Проверяет поведение open_cell при открытии нуля
    '''
    game = Game(5, 5, 3)
    game.hidden_field = [[1, 2, -1, 1, 0], 
                          [1, -1, 2, 1, 0], 
                          [1, 1, 1, 0, 0], 
                          [0, 0, 1, 1, 1], 
                          [0, 0, 1, -1, 1]]
    expected = [[False, False, False, True, True],
                [False, False, True, True, True],
                [False, False, True, True, True],
                [False, False, True, True, True],
                [False, False, False, False, False]]
    game.open_cell(2, 4)
    assert game.player_field == expected


def test_mines_counter():
    '''
    Проверяет корректность числа мин на поле
    '''
    game = Game(5, 5, 3)
    mines_count = 0
    for row in game.hidden_field:
        for cell in row:
            if cell == -1:
                mines_count += 1
    assert mines_count == 3


def test_mines_neighbors():
    '''
    Проверяет корректность расчета соседей-мин
    '''
    game = Game(5, 5, 3)
    for r in range(game.rows):
        for c in range(game.cols):
            if game.hidden_field[r][c] == -1:
                continue
            
            expected = 0
            for nr, nc in game.neighbors(r, c):
                if game.hidden_field[nr][nc] == -1:
                    expected += 1
            
            assert game.hidden_field[r][c] == expected