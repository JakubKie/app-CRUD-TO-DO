from .repos import TaskRepository, UserRepository
from .models import Task, User, StatusEnum, PriorityEnum
from typing import List


class TaskService:
  def __init__(self, task_repo: TaskRepository, user_repo: UserRepository):
    self.task_repo = task_repo
    self.user_repo = user_repo


def create_task(self, data: dict) -> Task:
  user = self.user_repo.get_by_id(data['user_id'])
  if not user:
    raise ValueError('User not found')

  task = Task(
    task_name=data['task_name'],
    user_id=data['user_id'],
    due_date=data.get('due_date'),
    status=StatusEnum(data.get('status')) if data.get('status') else StatusEnum.pending,
    priority=PriorityEnum(data.get('priority')) if data.get('priority') else PriorityEnum.medium
  )
  return self.task_repo.create(task)

def list_tasks(self) -> List[Task]:
  return self.task_repo.get_all()

def get_task(self, task_id: int) -> Task:
  task = self.task_repo.get_by_id(task_id)
  if not task:
    raise ValueError('Task not found')
  return task

def update_task(self, task_id: int, data: dict) -> Task:
  task = self.get_task(task_id)
  if 'task_name' in data:
    task.task_name = data['task_name']
  if 'status' in data:
    task.status = StatusEnum(data['status'])
  if 'due_date' in data:
    task.due_date = data['due_date']
  if 'priority' in data:
    task.priority = PriorityEnum(data['priority'])
  return self.task_repo.update(task)

def delete_task(self, task_id: int) -> None:
  task = self.get_task(task_id)
  return self.task_repo.delete(task)

class UserService:
  def __init__(self, user_repo: UserRepository):
    self.user_repo = user_repo

def create_user(self, data: dict) -> User:
  u = User(username=data['username'], role=data.get('role'))
  return self.user_repo.create(u)

def list_users(self):
  return self.user_repo.get_all()