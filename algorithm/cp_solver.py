""" cp-sat解决 基本fjsp问题"""
import collections
from ortools.sat.python import cp_model
from model.solver import Solver
from model.problem import Problem
from model.solution import Solution


task_type = collections.namedtuple('Task', 'start end dura')


class CPSolver(Solver):
    def __init__(self, name: str = 'cp-sat solver', max_time: int = 300):
        super().__init__(name)
        self.max_time = max_time

    def solve(self, prob: Problem):
        model, all_tasks, op_starts, op_ends, machine_intervals = CPSolver._create_mode(prob)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.max_time
        status = solver.Solve(model)

        print(f'=================status:{solver.StatusName(status)}')
        print(f'=================status:{status}')

        # 填充solution
        solution = Solution(prob)
        solution.makespan = solver.ObjectiveValue()
        solution.get_solution_from_cp(solver, all_tasks)

        for j, job in prob.jobs.items():
            print(f'job----{j}')
            for p in job.route:
                for m in prob.ops[p].process_time.keys():
                    task = all_tasks[j, p, m]
                    if solver.Value(task.dura) == 0:
                        continue
                    print(f'----p:{p}, m:{m}, start:{solver.Value(task.start)}, end:{solver.Value(task.end)}, dura:{solver.Value(task.dura)}')
        print('MAKESPAN: ', solver.ObjectiveValue())
        return solution

    @staticmethod
    def _create_mode(prob: Problem):
        jobs = prob.jobs
        ops = prob.ops
        machines = prob.machines
        M = prob.M
        md = cp_model.CpModel()

        # 创建区间变量
        x_jpm = {}
        all_tasks = {}
        machine_intervals = collections.defaultdict(list)
        op_starts = {}
        op_ends = {}
        for j, job in jobs.items():
            for p in job.route:
                op_starts[j, p] = md.NewIntVar(0, M, f'opstarts_{j}_{p}')
                op_ends[j, p] = md.NewIntVar(0, M, f'opends_{j}_{p}')
                for m, duration in ops[p].process_time.items():
                    suffix = f'_{j}_{p}_{m}'
                    x_jpm[j, p, m] = md.NewBoolVar('x' + suffix)

                    start_var = md.NewIntVar(0, M, 'startvar' + suffix)
                    end_var = md.NewIntVar(0, M, 'endvar' + suffix)

                    dura_var = md.NewIntVar(0, duration, 'duravar' + suffix)
                    # 没有选择该machine, 则dura_var=start_var=end_var=0
                    md.Add(dura_var <= M * x_jpm[j, p, m])
                    md.Add(start_var + end_var <= M * x_jpm[j, p, m])  # 易漏掉的约束, 保证start_var=end_var=0
                    # 选择了该machine, 则dura=duration
                    md.Add(dura_var <= duration + M * (1 - x_jpm[j, p, m]))
                    md.Add(dura_var >= duration + M * (x_jpm[j, p, m] - 1))

                    interval_var = md.NewIntervalVar(start=start_var, size=dura_var,
                                                     end=end_var, name='intervalvar'+suffix)
                    task = task_type(start=start_var, end=end_var, dura=dura_var)
                    machine_intervals[m].append(interval_var)
                    all_tasks[j, p, m] = task

        # 约束0, op_starts = max{task_starts}
        for j, job in jobs.items():
            for p in job.route:
                md.AddMaxEquality(op_starts[j, p],
                                  [all_tasks[j, p, m].start for m in ops[p].process_time.keys()])
                md.AddMaxEquality(op_ends[j, p],
                                  [all_tasks[j, p, m].end for m in ops[p].process_time.keys()])

        # 约束1, 每个job下各operation之间有先后关系
        for j, job in jobs.items():
            for i in range(len(job.route)-1):
                p1, p2 = job.route[i], job.route[i+1]
                md.Add(op_starts[j, p2] - op_ends[j, p1] >= 0)

        # 约束2, 每个operation只能由一台设备来加工
        for j, job in jobs.items():
            for p in job.route:
                md.Add(sum(x_jpm[j, p, m] for m in ops[p].process_time.keys()) == 1)

        # 约束2, 对同一个machine, 各operation时间没有重叠
        for m, intervals in machine_intervals.items():
            md.AddNoOverlap(intervals)

        # 设定目标, 最小makespan
        makespan = md.NewIntVar(0, M, 'makespan')
        md.AddMaxEquality(makespan, op_ends.values())
        md.Minimize(makespan)
        return md, all_tasks, op_starts, op_ends, machine_intervals
