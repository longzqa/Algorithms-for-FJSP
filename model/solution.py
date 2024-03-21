import collections
from model.problem import Problem


class Solution:
    def __init__(self, prob: Problem):
        """
        self._job_res = {
            job.id: [{'op_id': p, 'start': 0, 'interval': 0, 'end': 0, 'machine': 0}
                for p in job.route
            ]
            for job in prob.jobs.values()
        }

        self._machine_res = {
            m: [
                {'job_id': 0, 'op_id': 0, 'start': 0, 'interval': 0, 'end': 0}
            ]
            for m in prob.machines.keys()
        }
        """
        self.prob = prob
        self.makespan = 0
        self._job_res = collections.defaultdict(list)
        self._machine_res = collections.defaultdict(list)

    @property
    def job_res(self):
        res = {}
        for j, operations in self._job_res.items():
            _sorted_item = sorted(operations, key=lambda item: item['index'], reverse=False)
            res[j] = _sorted_item
        return res

    @property
    def machine_res(self, machine: int = None):
        if machine is not None:
            res = self._machine_res[machine]
            res = sorted(res, key=lambda item: item['start'], reverse=False)
            return res

        res = {}
        for m, tasks in self._machine_res.items():
            _sorted_item = sorted(tasks, key=lambda item: item['start'], reverse=False)
            res[m] = _sorted_item
        return res

    def get_solution_from_cp(self, solver, all_tasks):
        if not all_tasks:
            return
        for (j, p, m), task in all_tasks.items():
            if solver.Value(task.dura) == 0:
                continue
            self._job_res[j].append({'op_id': p,
                                     'index': self.prob.jobs[j].route.index(p),
                                     'start': solver.Value(task.start),
                                     'interval': solver.Value(task.dura),
                                     'end': solver.Value(task.end),
                                     'machine': m})
            self._machine_res[m].append({'job_id': j,
                                         'op_id': p,
                                         'start': solver.Value(task.start),
                                         'interval': solver.Value(task.dura),
                                         'end': solver.Value(task.end)})

        print()
