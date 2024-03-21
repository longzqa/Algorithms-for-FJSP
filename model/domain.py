class Base:
    def __init__(self, _id: int) -> None:
        """ An instance with an ID."""
        self.id = _id

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.id})'


class Job(Base):
    def __init__(self, _id: int, _type: str, route: list[int]):
        super().__init__(_id)
        self.type = _type
        self.route = route  # 工序执行流程


class Operation(Base):
    def __init__(self, _id: int, job: Job, process_time: dict[int, int]):
        super().__init__(_id)
        self.job = job
        self.process_time = process_time  # 设备id: 执行时间

        # self.machine = None
        # self.duration = None
        # self.start_time = 0
        # self.end_time = 0


class Machine(Base):
    def __init__(self, _id: int, capacity: int = 1, _type: str = ''):
        super().__init__(_id)
        self.capacity = capacity  # 可以同时处理的工序数量
        self.type = _type



