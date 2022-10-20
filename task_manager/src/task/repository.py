from abc import ABC, abstractmethod
from uuid import UUID

from src.task.model import Task, TaskStatus


class TaskNotFound(Exception):
    def __init__(self, id: UUID) -> None:
        super().__init__(f"Task {id} not found")


class TaskRepository(ABC):
    def raise_for_not_found(self, id: UUID):
        if self.get(id) is None:
            raise TaskNotFound(id)

    @abstractmethod
    def add(self, task: Task):
        pass

    @abstractmethod
    def assign(self, task_id: UUID, assignee_id: UUID): 
        pass

    @abstractmethod
    def update_info(self, task: Task):
        pass

    @abstractmethod
    def set_status(self, task_id: UUID, status: TaskStatus):
        pass

    @abstractmethod
    def get(self, task_id: UUID) -> Task | None:
        pass

    @abstractmethod
    def all(self) -> list[Task]:
        pass


class InMemoryRepository(TaskRepository):
    def __init__(self) -> None:
        super().__init__()
        self.data: dict[UUID, Task] = {} 

    def add(self, task: Task):
        self.data[task.id] = task

    def assign(self, task_id: UUID, assignee_id: UUID):
        self.raise_for_not_found(task_id)
        self.data[task_id].assignee = assignee_id

    def update_info(self, task: Task):
        self.raise_for_not_found(task.id)
        self.data[task.id] = task

    def set_status(self, task_id: UUID, status: TaskStatus):
        self.raise_for_not_found(task_id)
        self.data[task_id].status = status

    def get(self, task_id: UUID) -> Task | None:
        task = self.data.get(task_id)
        if task is None:
            raise TaskNotFound(task_id)
        
        return task

    def all(self) -> list[Task]:
        return list(self.data.values())

