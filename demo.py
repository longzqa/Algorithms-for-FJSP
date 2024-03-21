import os
from model.problem import Problem
from algorithm.cp_solver import CPSolver
from utils.data_parser import get_instance


home = os.path.dirname(os.path.abspath(__file__))


def main():
    test_dt_dir = os.path.join(home, 'instances')
    aa = os.path.join(test_dt_dir, 'Brandimarte_Data', 'Text', 'MK01.fjs')
    job_info, machine_info = get_instance(aa)
    prob = Problem(job_info, machine_info)
    solver = CPSolver(max_time=6)
    res = solver.solve(prob)
    print()


if __name__ == '__main__':
    main()

