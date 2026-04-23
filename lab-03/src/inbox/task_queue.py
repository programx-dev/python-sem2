from collections.abc import Iterable
from typing import Callable
from src.contracts.task import Task

class TaskQueue:
    def __init__(self, tasks: Iterable[Task], filters: list[Callable[[Task], bool]] | None = None):
        self._tasks = tasks
        self._filters = filters or []
    
    def __iter__(self):
        return TaskQueueIterator(iter(self._tasks), self._filters)
    
    def filter_by(self, filter: Callable[[Task], bool]):
        return TaskQueue(self._tasks, self._filters + [filter])
    
class TaskQueueIterator:
    def __init__(self, tasks: Iterable[Task], filters: list[Callable[[Task], bool]] | None = None):
        self._iterator = iter(tasks)
        self._filters = filters or []

    def __iter__(self) -> "TaskQueueIterator":
        return self
    
    def __next__(self) -> Task:
        for task in self._iterator:
            if all(f(task) for f in self._filters):
                return task
            
        raise StopIteration