import collections
from .domain import Job, Machine, Operation


class Problem:
    def __init__(self, job_info: dict, machine_info: dict):
        """

        :param job_info:
        :param machine_info:
        :return:


        EXAMPLE job_info
        -----------------
        {
            4: {  # job_id
                'product_type': 'A',  # 所属的产品类型
                'route': [4, 2, 1],  # 工艺流程, 元素为operation_id
                'process_time': {  # 各工序在不同设备上的处理时间
                    4: {99: 5, 98: 4},
                    2: {99: 4, 98: 7}
                }
            }
        }

        EXAMPLE machine_info
        ---------------------
        {
            5: {  # machine_id
                'machine_type': 'stove',  # 设备类型
                'capacity': 1
            }
        }
        """
        self.M = None
        self.jobs: dict[int, Job] = {}
        self.ops: dict[int, Operation] = {}
        self.machines: dict[int, Machine] = {}
        self._create_jobs_and_operations(job_info)
        self._create_machines(machine_info)

    def _create_jobs_and_operations(self, job_info: dict):
        if not job_info:
            return
        jobs = {}
        operations = {}
        M = 0
        for _id, job_dict in job_info.items():
            job = Job(_id, job_dict.get('product_type', ''), job_dict.get('route', []))
            jobs[_id] = job
            process_time = job_dict.get('process_time', {})
            for op_id, times in process_time.items():
                operations[op_id] = Operation(op_id, job, times)
                M += sum(times.values())
        self.jobs = jobs
        self.ops = operations
        self.M = M

    def _create_machines(self, machine_info: dict):
        if not machine_info:
            return
        machines = {}
        for _id, machine_dict in machine_info.items():
            machines[_id] = Machine(_id, machine_dict.get('capacity', 1), machine_dict.get('machine_type', ''))
        self.machines = machines
