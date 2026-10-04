import pytest
from mine_field import Game

def test_neighbors():
    game = Game(3, 3, 0)
    result = game.neighbors(1, 1)
    assert len(result) == 8