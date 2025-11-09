import datetime

from taskStateEnum import TaskStatus

class VmTask:
    def __init__(self, task_id, name: str, description: str, status: TaskStatus, created_at: datetime.datetime, updated_at: datetime.datetime, is_deleted=False):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.status = status
        self.is_deleted = is_deleted
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"ID: {self.task_id}, Name: {self.name}, Description: {self.description}, Status: {self.status.name}, Is Deleted: {self.is_deleted}, Created At: {self.created_at}, Updated At: {self.updated_at}"