import pytest
import collections
import numpy as np
import pandas as pd


def _create_case(job_num=5, proc_num=4, machine_num=4):
    product_types = np.array(['A', 'B', 'C'])

    machines = np.arange(200, 200+machine_num, 1, dtype=int)
    jobs = np.arange(100, 100+job_num, 1, dtype=int)
    operations = np.arange(900, 900+proc_num, 1, dtype=int)  # process
    job_types = np.random.choice(product_types, size=len(jobs))  # 每个job对应的产品类型

    # <editor-fold, desc="machine_info">
    machine_info = {
        _id: {'machine_type': '', 'capacity': 1}
        for _id in machines
    }

    # </editor-fold>

    # <editor-fold, desc="job_info">
    # proc_times: dict[int, pd.DataFrame] = {}  # 工序处理时间
    job_info = collections.defaultdict(dict)
    for i, j_id in enumerate(jobs):
        times = pd.DataFrame(np.zeros([proc_num, machine_num], dtype=int), operations, machines)
        times[:] = np.random.randint(0, 5, size=(proc_num, machine_num))
        noneed_ops = times[(times==0).all(axis=1)].index  # 去除在各设备上加工时间都是0的operation

        _route = operations.copy()
        np.random.shuffle(_route)
        route = []
        for op in _route:
            if op in noneed_ops:
                continue
            route.append(int(op))

        process_time = collections.defaultdict(dict)
        for op in route:
            process_time[op] = {m: times.loc[op, m] for m in machines if times.loc[op, m] != 0}

        job_info[j_id] = {'product_type': job_types[i],
                          'route': route,
                          'process_time': process_time}

    # </editor-fold>

    return job_info, machine_info


@pytest.fixture
def random_case():
    res = []
    for i in range(3):
        res.append(_create_case())
    return res


if __name__ == '__main__':
    j_info, m_info = _create_case(2, 2, 2)
    print()
