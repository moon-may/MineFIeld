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