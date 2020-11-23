from aocd.models import Puzzle
from aocd.get import get_day_and_year

class PuzzleWithTests(Puzzle):
    def __init__(self):
        day, year = get_day_and_year()
        super().__init__(year, day)