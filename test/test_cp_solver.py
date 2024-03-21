from model.problem import Problem
from algorithm.cp_solver import CPSolver


def test_operation_priority(random_case):
    """ 测试一个job下的各operation, 是否按照route的顺序来先后执行"""
    cases = random_case
    for case in cases:
        job_info, machine_info = case
        prob = Problem(job_info, machine_info)
        solver = CPSolver()
        solution = solver.solve(prob)

        job_res = solution.job_res
        for j_id, ops in job_res.items():
            for i in range(len(ops)-1):
                op1, op2 = ops[i], ops[i+1]
                assert op1['end'] <= op2['start']
                assert op1['interval'] > 0


def test_operation_overlap(random_case):
    """ 测试同一个machine上的各工序，时间区间是否存在重叠"""
    cases = random_case
    for case in cases:
        job_info, machine_info = case
        prob = Problem(job_info, machine_info)
        solver = CPSolver()
        solution = solver.solve(prob)

        machine_res = solution.machine_res
        for m_id, ops in machine_res.items():
            for i in range(len(ops) - 1):
                op1, op2 = ops[i], ops[i + 1]
                assert op1['end'] <= op2['start']
                assert op1['interval'] > 0
