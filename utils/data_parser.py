import os


def _parse_fjsp_file(path):
    """
    解析fjsp文件
    :param path:
    :return:

    EXAMPLE return
    ----------------
    {
        'machine_num': 5,  # 5个machine
        ’jobs‘: [
            0: [  # operation0
                {'machine': 1, 'process_time': 5},  # 该operation在machine1上处理时间为5
                ...
            ]
        ]
    }

    """
    file = open(path, 'r')

    fir_line = file.readline()
    fir_line_vals = list(map(int, fir_line.split()[0:2]))

    job_num = fir_line_vals[0]
    machine_num = fir_line_vals[1]

    jobs = []

    for i in range(job_num):
        cur_line = file.readline()
        curr_line_vals = list(map(int, cur_line.split()))

        operations = []

        j = 1
        while j < len(curr_line_vals):
            k = curr_line_vals[j]
            j = j+1

            operation = []

            for ik in range(k):
                machine = curr_line_vals[j]
                j = j+1
                proc_time = curr_line_vals[j]
                j = j+1

                operation.append({'machine': machine, 'process_time': proc_time})
            operations.append(operation)
        jobs.append(operations)

    file.close()

    return {'machine_num': machine_num, 'jobs': jobs}


def get_instance(path):
    """
    获取测试数据
    :param path:
    :return: job_info, machine_info

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
    if not path:
        return
    fjsp_data: dict = _parse_fjsp_file(path)

    # <editor-fold, desc="machine_info">
    machine_num = fjsp_data['machine_num']
    machine_info = {
        _id: {'machine_type': '', 'capacity': 1}
        for _id in range(machine_num)
    }

    # </editor-fold>

    # <editor-fold, desc="job_info">
    job_lst = fjsp_data['jobs']
    job_info = {}
    for j_id, job_data in enumerate(job_lst):
        job_route = []
        process_time = {}
        for i, op_data in enumerate(job_data):
            job_route.append(i)
            process_time[i] = {time_info['machine']: time_info['process_time']
                               for time_info in op_data}
        job_info[j_id] = {'product_type': '', 'route': job_route, 'process_time': process_time}

    # </editor-fold>

    return job_info, machine_info


if __name__ == '__main__':
    test_dt_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instances')
    aa = os.path.join(test_dt_dir, 'Brandimarte_Data', 'Text', 'MK01.fjs')
    res = get_instance(aa)
    print()
