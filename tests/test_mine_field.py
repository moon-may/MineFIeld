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