# from .solution import Solution
from .problem import Problem


class Solver:
    def __init__(self, name: str = None):
        self.name = name
        self.used_time = 0
        # self.solution = Solution()

    def solve(self, prob: Problem):
        raise NotImplementedError('no solver implemented!!!')
